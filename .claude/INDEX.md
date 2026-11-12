# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11255  GET              /                                                dashboard
 13312  GET              /api/abo/status                                  api_abo_status
 13266  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 12043  GET              /api/automation/status                           api_automation_status
 12065  POST             /api/automation/toggle                           api_automation_toggle
 21916  GET              /api/channel/categories                          api_channel_categories
 21922  POST             /api/channel/set                                 api_channel_set
 21769  GET              /api/channels/status                             api_channels_status
 21443  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21426  GET              /api/clips                                       api_clips
 21472  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21344  GET              /api/debug/threads                               api_debug_threads
 13277  GET              /api/events                                      api_events
 12756  GET              /api/events/stream                               api_events_stream
 12583  GET              /api/health                                      api_health
 21385  POST             /api/highlights/config                           api_highlights_config
 11185  POST             /api/login                                       dashboard_login_submit
 13602  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12671  GET              /api/notify/status                               api_notify_status
 12682  POST             /api/notify/test                                 api_notify_test
 13366  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13343  GET              /api/proxy/trend                                 api_proxy_trend
 21492  GET              /api/tts/<fn>                                    api_tts_file
 22280  GET              /api/upload_window                               api_upload_window
 12873  GET              /archive/<int:eid>/download                      archive_download
 12901  GET              /download/<int:recording_id>                     download
 12830  GET              /health                                          health
 21218  GET              /healthz                                         healthz
 11176  GET              /login                                           dashboard_login_page
 11210  GET              /logout                                          dashboard_logout
 11217  GET              /manifest.webmanifest                            pwa_manifest
 22253  GET              /overlay                                         overlay_page
 11241  GET              /pwa-icon-<variant>.png                          pwa_icon
 11227  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   997  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   868  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   848  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   886  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1235  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1267  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   950  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   930  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1103  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1151  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1202  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1061  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   905  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   417  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   408  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   374  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   359  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   179  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   130  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   200  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   227  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   320  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   264  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   282  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   187  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   125  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   139  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   154  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   222  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   242  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   269  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   225  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   247  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   174  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   131  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   181  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   229  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   212  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   121  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   539  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   591  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   613  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   552  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   578  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   415  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   405  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   440  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2285  /about                  Ueber diesen Bot
   981  /ai                     
  2285  /aireset                KI-Kontext zuruecksetzen
  1399  /ask                    
  1082  /assign_role            
  1132  /ban                    
  2240  /botstats               
  2285  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2285  /bulkadd                Mehrere User auf einmal tracken · a b c
  2285  /cleanup                Alte Aufnahmen aufraeumen
  1665  /clearwarns             
  2204  /clip                   
  2189  /clipoftheweek          
  1535  /clips                  
  2285  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1037  /create_category        
  1008  /create_channel         
  1072  /create_group           
  1047  /create_role            
  1023  /create_voice           
  1276  /daily                  
  2285  /diag                   Vollstaendige Diagnose
  2285  /einnahmen              Einnahmen und Spenden
  1428  /event                  
  1470  /events                 
  1575  /follow                 
  1564  /help                   
  1122  /kick                   
  1248  /leaderboard            
  2285  /live                   Live-Status sofort pruefen · @user
  1522  /livenow                
  2285  /logs                   Letzte Fehler aus dem Log
  2285  /pause                  Tracking pausieren · @user
  1550  /post_test              
  1360  /profile                
  1154  /purge                  
  2285  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2285  /quota                  Speicher-Quota
  1235  /rank                   
  1510  /recstatus              
  1092  /remove_role            
  2285  /report                 Azrael-Sentinel-Wochenreport
   994  /restream_status        
  2285  /resume                 Tracking fortsetzen · @user
  1102  /set_channel_perms      
  1197  /setup_community        
  1214  /setup_targets          
  1496  /spenden                
  1607  /stats                  
   953  /status                 
  2285  /stoprec                Laufende Aufnahme sauber beenden · @user
  1703  /streaminfo             
  2285  /summary                Tageszusammenfassung
  2285  /sysres                 System-Ressourcen
  2285  /teststream             Recorder-Selbsttest · @user
  2285  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1142  /timeout                
  1675  /topstreamers           
  2285  /topusers               Top-Streamer nach Aufnahmen
   883  /track                  
  2285  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   966  /tracklist              
  1589  /unfollow               
  2285  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   915  /untrack                
  1628  /warn                   
  1651  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2452  on_member_join
  2409  on_message
  2306  on_raw_reaction_add
  2487  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1780-1831   _award_xp
   537-564    _bereich_umziehen
   484-494    _clip_kopieren
  2002-2031   _clip_week_leader
  2055-2069   _clipoftheweek_loop
  2604-2666   _community_events_loop
  1737-1759   _dc_client
  1762-1771   _dc_offen
  2706-2741   _disc_automod_check
   410-415    _disc_sprache_setzen
  1834-1882   _discord_ai_automod
   686-725    _discord_automod
  1885-1905   _discord_azrael_reply
  2072-2563   _discord_run_once
   245-303    _discord_start
   306-360    _ensure_discord_invite
  2569-2601   _ensure_error_channel
   431-444    _ensure_rank_roles
   846-860    _ensure_team_roles
  2669-2699   _error_channel_loop
   735-739    _guard
   655-683    _handle_voice_ai
   418-428    _is_admin
   509-534    _link_video
  1950-1961   _liveboard_loop
   742-775    _on_level_up
   651-652    _par_chat_id
  2034-2052   _post_clip_of_week
  1964-1982   _post_weekly_digest
   447-473    _provision_base_channels
  1502-1596   _reg_betrieb
  1168-1265   _reg_community_setup
  1268-1349   _reg_daily_profil
  1392-1489   _reg_frage_events
   940-996    _reg_info
  1114-1165   _reg_moderation
  1352-1389   _reg_profil
  1063-1111   _reg_rollen
   999-1060   _reg_server
  1492-1499   _reg_spenden
  1599-1686   _reg_streamer
  1689-1734   _reg_system
   874-937    _reg_tracking
   810-843    _run_tg_handler
   638-648    _tracked_usernames
   162-224    _uebernehmen
   497-506    _umzugsmarken
  1914-1947   _update_liveboard
  1985-1999   _weekly_digest_loop
   476-481    _ziel_guild
   567-609    _ziele_abgleichen
   618-635    _ziele_sync_loop
   612-615    _ziele_takt_min
   227-230    starte
```

## Top-Level-Symbole in bot.py (611 Funktionen, 4 Klassen)

```
 27473-27495  _abbruch_datenbank_unlesbar
  2844-2845   _abo_key
  2865-2883   _abo_probe_dump
 27595-27611  _abschied_wachen
 27614-27632  _abschluss
 17475-17482  _ad_allowlist
 18637-18643  _agent_for
 18646-18662  _ai_telemetry
 19159-19177  _alert
 23148-23198  _alert_monitor_loop
 19864-19921  _alte_beilagen_einsammeln
 23580-23642  _announce_loop
  3796-3806   _anthropic_key
  3813-3815   _anthropic_model
 10744-10747  _arg_int
  2836-2841   _as_dict
 27159-27168  _async_exc_handler
 19348-19370  _audio_tap_cmd
 20384-20443  _audio_tap_melden
 19384-19408  _audio_tap_sammler
 10090-10127  _aufnahme_beim_stopp_sichern
 19806-19827  _aufnahme_chat_ausklang
 19790-19803  _aufnahme_chat_beginnen
 19949-19970  _aufnahme_chat_dienst
 20143-20196  _aufnahme_chat_einarbeiten
 19785-19787  _aufnahme_chat_modus
 19973-20022  _aufnahme_chat_nachtrag
 19830-19861  _aufnahme_chat_vormerken
 19940-19946  _aufnahme_chat_wecken
 26283-26285  _aufnahme_deckel
 20025-20046  _aufnahme_fertigmachen
 23817-23870  _aufnahme_nach_discord
 10130-10148  _aufnahme_platz_frei
 10033-10060  _aufnahme_verteilen
 27559-27579  _aufnahmen_abschliessen
 27498-27556  _aufraeumen
 11018-11087  _auth_cookie
 10974-11014  _auth_guard
  2071-2076   _auto_on
 21070-21088  _auto_restream_loop
 14947-14989  _avatar_frames_laden
 17525-17538  _azrael_brain_kontext
 24776-24791  _azrael_broadcast_reply
 24676-24698  _azrael_chat_reply
 24648-24673  _azrael_chat_should_reply
 24704-24706  _azrael_gate_cfg
 18667-18681  _azrael_live_state
 22166-22180  _azrael_overlay_state
 19041-19095  _azrael_proactive_loop
 18485-18541  _azrael_reaction_to_chats
 24709-24716  _azrael_reply_all_chats
 24635-24645  _azrael_self_names
 24744-24773  _azrael_send_to
 14908-14944  _azrael_spricht
 15255-15268  _azrael_stimme_stumm
 18687-18708  _azrael_system
 23282-23285  _backup_active
 23363-23376  _backup_loop
  5554-5577   _betreiber_pruefen
 26372-26376  _betrieb
 27232-27241  _brain_crowdsec_snap
 27400-27403  _brain_db_health
 23069-23078  _brain_growth_loop
 11434-11461  _brain_growth_snapshot
  2755-2789   _brain_hint_delay
 27304-27339  _brain_moderation_snap
  6828-6856   _brain_notify
 27406-27428  _brain_recording_snap
 27244-27301  _brain_restream_health
 27431-27444  _brain_tiktok_status_snap
 12735-12752  _browser_push
  6868-6955   _build_daily_summary
 15302-15306  _build_restream_cmd
  5580-5607   _can_stop_tracking
  2184-2206   _capture_set_cookies
 13420-13423  _cfg_get
 13426-13428  _cfg_set
 21877-21912  _channel_set_all
 13999-14002  _chat_connected
 14005-14021  _chat_disconnected
 19934-19937  _chat_einarbeiten_async
  9524-9554   _chat_is_forum
 19754-19779  _chat_listener_abbauen
  9696-9731   _chat_migriert
  9734-9735   _chat_migriert_async
 14041-14043  _chat_sanitize
 13984-13996  _chat_stat
 14024-14027  _chat_stats_snapshot
  4119-4131   _check_ai_models_sync
 11716-11759  _classify_pool_anonymity
 11762-11779  _classify_pool_anonymity_bg
   919-941    _claude_chat_sync_metered
 10776-10782  _client_ip
 24275-24289  _clip_chat_ass
 23726-23760  _clip_prune
 23763-23773  _clip_recfile_for
 24195-24263  _clip_schneiden
 24292-24298  _clip_should_velocity
 23873-23958  _clip_to_discord
 20114-20119  _clips_abwarten
  4000-4009   _close_ai_session
 24822-24837  _cohost_broadcast
 24807-24808  _cohost_cfg
 24863-24875  _cohost_fire_highlight
 24811-24819  _cohost_gate
 24840-24860  _cohost_highlight
 11364-11366  _conv_messages
  7252-7313   _cookie_alarm_loop
  2274-2275   _cookie_autofetch_info
  2258-2262   _cookie_autorefresh_info
 26833-26855  _cookie_bezug_loop
 26858-26883  _cookie_bezug_runde
  2161-2165   _cookie_header
 10785-10790  _cookie_sicher
  2287-2301   _cookies_selbst_holen
  4340-4342   _create_index_safe
 22612-22726  _crowdsec_status
 22558-22609  _crowdsec_via_lapi
 22462-22480  _cscli_bin
 22489-22502  _cscli_path
  7136-7163   _daily_summary_loop
 22520-22537  _darf_journal_lesen
  3321-3346   _darf_ytdlp_nachschlagen
 12916-12937  _dashboard_adresse
 10805-10809  _dashboard_hostnamen
  1523-1553   _dashboard_trackings_umziehen
 24266-24272  _datei_weg
 23122-23145  _db_maintenance_loop
  7086-7133   _db_vacuum_loop
 17498-17522  _detect_foreign_ad
  1751-1762   _diag_path_owner
 18946-18991  _director_finalize
 20373-20380  _director_for
 18895-18943  _director_mark
 24108-24111  _disc_state_get
 24114-24121  _disc_state_set
 23050-23059  _discord_bot_starten
 23013-23024  _discord_einladung_merken
 23062-23066  _discord_invite
 23027-23047  _discord_kontext
 24069-24105  _discord_live_thread
 19098-19110  _discord_notify
 22985-23010  _discord_ops_alert
 23969-24065  _discord_post_user
 23645-23651  _discord_stop
  7166-7247   _disk_alarm_loop
 26704-26755  _disk_autoclean
 27014-27027  _disk_guard_loop
 14886-14893  _drossel_hoeher
 14882-14883  _drossel_stufe
 14896-14904  _drossel_zuruecksetzen
 13093-13095  _dump_all_threads
 26379-26393  _einstellungen_startzeile
 11642-11705  _enrich_proxies_with_geo
  2330-2391   _ensure_cookie_file_netscape
  9625-9628   _ensure_notify_topic
 11886-11923  _ensure_proxy_ready
  9564-9587   _ensure_topic
   760-762    _env_int
   765-767    _env_int_range
 19143-19156  _event_webhook
 13767-13780  _evolution_loop
  6269-6303   _extract_file_payload
  2463-2465   _extract_urls_from_streamurl_node
 22505-22512  _f2b_sudo_hint
  1509-1520   _fanout_ziele
 27635-27698  _fatal_vom_botteil
 26288-26303  _fd_grenze_anheben
  5014-5024   _fehler_text
 11543-11561  _fetch_proxy_list
 19723-19751  _fetch_tiktok_room_id
   845-848    _ff_cmd
 20127-20140  _ffprobe_masse
 14830-14846  _fifo_schreiber_wecken
 14640-14645  _find_chromium
  3716-3718   _find_external_recorder
  2468-2470   _find_stream_urls
 13471-13496  _fire_webhooks
  8185-8195   _fork_safe
   952-965    _freeai_chat_sync_metered
 22551-22555  _geo_lookup_ips
  3988-3997   _get_ai_session
  8013-8053   _get_live_info
  3165-3172   _get_resolve_semaphore
  8712-9133   _handle_single_tracking
 26488-26490  _hb
 26493-26510  _hb_while
 21329-21340  _healthz_fuer_aufrufer
 26534-26562  _heap_zurueckgeben
 11091-11108  _herkunft_guard
 14055-14057  _highlight_cfg
 14060-14089  _highlight_observe
 14691-14699  _htmlov_bild_schreiben
 14669-14688  _htmlov_dauerbrowser
 14648-14666  _htmlov_screenshot_cmd
 19410-19420  _httpx_proxy
 13504-13516  _in_quiet_hours
 27459-27470  _init_db_oder_abbruch
 28285-28316  _install_fast_eventloop
 10639-10693  _install_fast_json
 13098-13114  _install_faulthandler
 21121-21130  _intel_ensure_schema
 21173-21208  _intel_index_loop
 21142-21157  _intel_index_one
 21133-21139  _intel_semantic
  5539-5552   _is_authorized
  8538-8559   _is_dead
  2453-2455   _is_hevc
 22540-22542  _is_private_ip
  1970-1977   _is_process_running
  6858-6865   _is_quiet_hours
  1411-1420   _is_upload_window
  4879-4894   _iso
 10793-10802  _ist_lokal
 10728-10741  _json_error_handler
  7080-7081   _kick_broadcaster_id
  8413-8420   _kick_cluster_gefunden
  8348-8410   _kick_cluster_weiter
  6992-7034   _kick_follower_count
  6976-6979   _kick_slug
 12548-12555  _kick_user_token
  8318-8345   _kick_ws_pause
 27447-27456  _kickmod_boot
  4424-4427   _kind_from_filename
 26799-26802  _lagebild_discord_aufnahme
 26812-26816  _lagebild_kick_chat
 26805-26809  _lagebild_overlay
 26819-26821  _lagebild_spendenziel
 26786-26796  _lagebild_upload
 13533-13535  _latest_popularity
  1907-1916   _laufstand
 26974-27011  _laufstand_loop
 26412-26450  _leistung_erheben
  7887-7914   _link_video_senden
  8699-8710   _live_check_frist_melden
  2899-2912   _live_ohne_stream
 20779-20828  _live_react_loop
 20446-20768  _live_react_worker
  3564-3678   _live_status_aufloesen
 18544-18555  _live_transcript_push
 20770-20777  _live_users
 18994-19038  _living_title_loop
 23288-23360  _local_backup_scan
  4819-4842   _lock_update
 10710-10724  _log_5xx
 26453-26485  _log_schleuse_pruefen
   835-842    _log_sicher
 15314-15326  _looks_like_codec_err
 15309-15311  _looks_like_source_expired
  8236-8266   _loop_fehler
 13118-13127  _loop_heartbeat
 26194-26227  _loop_lag_monitor
 26241-26261  _loop_stockung_melden
 26264-26274  _loop_takt_starten
 13130-13203  _loop_watchdog_thread
 18421-18438  _loyalty_add
 18412-18418  _loyalty_get
 18441-18449  _loyalty_top
  5221-5240   _manual_status
  8561-8562   _mark_dead
 12162-12178  _marketing_loop
 24723-24741  _maybe_handle_command
 27113-27137  _maybe_hype_clip
 23695-23723  _meme_klassifizieren
 20049-20111  _meme_zusammenschnitt
  4327-4332   _migrate_columns
 25005-25016  _mod_is_exempt
 25019-25024  _mod_warn_first
 25027-25030  _mod_warn_text
 13824-13843  _modlog
 13807-13821  _modlog_schreiben
  1107-1109   _multistream_targets
  3349-3385   _nachschlag_ytdlp
  8198-8199   _nc_create_subprocess_exec
  8202-8203   _nc_create_subprocess_shell
 12485-12502  _news_loop
 13866-13868  _normalize_ingest
  2686-2703   _note_check_duration
  9619-9622   _notify_topic_name
  2890-2896   _offline_ergebnis
  3388-3411   _ohne_url_melden
 18570-18578  _oracle_memories
 18844-18878  _oracle_memorize
 18581-18594  _oracle_persona
 18563-18567  _oracle_recent_text
 14264-14265  _ov_atomic_write
 14255-14257  _ov_bar
 17401-17413  _ov_clip_text
 14260-14261  _ov_oneline
 22217-22246  _overlay_push
 14594-14637  _overlay_render_size
 13935-13939  _overlay_session_reset
 22182-22184  _overlay_src_ok
 14274-14286  _overlay_takt
 17485-17495  _own_invites
 14589-14591  _parse_size
 22734-22814  _parse_ssh_attacks
  7563-7596   _pause_resume_cmd
  2212-2256   _persist_refreshed_cookies
  2115-2147   _pick_checked_pull_proxy
 10859-10874  _pin_auth_value
 10963-10964  _pin_clear_fail
 10927-10930  _pin_global_gesperrt
 10880-10891  _pin_hmac_schluessel
 10933-10940  _pin_locked
 10943-10960  _pin_note_fail
 10894-10915  _pin_ok
 22010-22035  _piper_pick_model
 22095-22160  _piper_say
 13433-13468  _post_json_threaded
 14568-14586  _probe_video_size
  1998-2015   _proc_is_recorder
 11855-11883  _proxy_pool_refresh_loop
  2081-2112   _proxy_report_recording
  9272-9353   _pruef_runde
  9231-9269   _pruefstand_melden
 26323-26334  _pruefung_verworfen
 13083-13085  _prune_stall_dumps
 12232-12404  _public_stats
  2278-2284   _pull_proxy_still
 19114-19140  _push_notify
 11155-11157  _pwa_dir
 11612-11627  _quick_validate_proxy
 13499-13501  _quiet_hours_config
 11120-11153  _rate_guard
  2915-2943   _raumsperre_fragen
 18382-18388  _react_warn
  8100-8139   _reap_proc
 10812-10828  _rebinding_melden
  9963-10030  _rec_auto_abschalten
  9910-9960   _rec_frueh_getrennt
  9775-9855   _rec_kategorie_melden
  9858-9907   _rec_totstreak_fortschreiben
  2726-2748   _record_check_outcome
   830-832    _redact_stream_urls
 11782-11852  _refresh_proxy_pool
  2503-2594   _resolve_via_html
  2946-3142   _resolve_via_webcast_api_v2
  3210-3297   _resolve_via_ytdlp
 24332-24461  _resolve_youtube_ingest
  2479-2500   _resolver_stumm
 13918-13929  _restream_active_sources
 14992-15119  _restream_avatar_feeder_start
 15122-15132  _restream_avatar_feeder_stop
 20199-20337  _restream_chat_guardian
 14092-14164  _restream_chat_push
 14241-14250  _restream_chat_push_async
 27342-27397  _restream_durchreicher
 14702-14827  _restream_html_overlay_start
 14849-14869  _restream_html_overlay_stop
 13877-13900  _restream_overlay_files
 20832-20864  _restream_platform_state
 21032-21067  _restream_resume_after_restart
 14195-14212  _restream_soll_schreiben
 14215-14238  _restream_status_schreiben
 15180-15252  _restream_tts_enqueue_wav
 14530-14562  _restream_tts_feeder
 14527-14528  _restream_tts_fifo_path
 15135-15162  _restream_tts_start
 15164-15178  _restream_tts_stop
 20870-21029  _restream_verify_loop
 23253-23265  _retention_loop
 23247-23250  _retention_scan
  2847-2849   _room_is_abo
  6307-6424   _run_ai_call
 13226-13239  _run_async_from_flask
 22545-22548  _run_priv
 28273-28281  _run_selfcheck_and_exit
 23268-23279  _s3_client
  8588-8658   _safe_send
  5147-5163   _sample_net_throughput
  2792-2822   _schedule_next_check
 23201-23244  _scheduler_loop
  4335-4337   _schema_pk
 13243-13248  _scraper_session
 25033-25072  _screen_full
 12599-12636  _sec_headers
  2458-2460   _select_stream_from_data_section
 27990-28270  _selfcheck
  9631-9665   _send_live_notice
  1434-1438   _should_defer_upload
 23776-23814  _shrink_for_discord
 11160-11172  _sicheres_ziel
 23081-23119  _sicherheits_erinnerung_loop
 27034-27051  _sign_health_check
 27054-27073  _sign_health_loop
  4897-4922   _sitzung_bestimmen
 21314-21322  _sparen_lage
  8215-8226   _spawn
 28704-28734  _spawn_from_flask
 26337-26343  _speicher_maps
 26346-26361  _speicher_pflegen
 19422-19720  _start_chat_listener
 26306-26320  _start_gesperrt
 13206-13223  _start_loop_watchdog
 12431-12480  _stats_loop
 12410-12413  _stats_output_path
 12416-12428  _stats_write
 22047-22061  _stimme_saubern
 22068-22092  _stimme_schon_gesagt
  9212-9228   _storage_cleanup_loop
 27093-27100  _story_for
  3741-3747   _stream_url_expiry
  3749-3754   _stream_url_ttl
 17448-17455  _streamer_persona_get
 23385-23537  _system_backup
 23546-23576  _system_backup_loop
 13043-13061  _task_auf_bot_schleife
 25870-25886  _telegram_befehlsmenue
  8269-8315   _telegram_polling_fehler
  1479-1506   _telegram_ziele
 11564-11603  _test_proxy
 12110-12126  _testpush_resolve_live
 20122-20124  _text_schreiben
  9683-9693   _tg_migriert_laden
  9679-9680   _tg_migriert_pfad
  8564-8585   _tg_sprache_setzen
  9493-9503   _tg_topics_load_into_mem
  9490-9491   _tg_topics_path
  9505-9512   _tg_topics_save
 10831-10841  _token_ok
  9590-9606   _topic_anlegen
  9515-9522   _topic_forget
 13519-13530  _tracking_max_duration
  4632-4646   _tracking_remove_cleanup
  4663-4675   _tracking_resume_cleanup
  1809-1832   _try_attach_file_handler
 22037-22045  _tts_cleanup
 12086-12090  _tunnel_effective
 26758-26778  _tunnel_lage
 26919-26971  _tunnel_wacht_loop
 21536-21589  _twitch_channel_status
 25075-25223  _twitch_chat_loop
 24127-24140  _twitch_clip_versuchen
 24886-24992  _twitch_eventsub_loop
  1599-1634   _upload_queue_abarbeiten
  1457-1477   _upload_queue_add
  1570-1572   _upload_queue_count
  1440-1449   _upload_queue_load
  1637-1659   _upload_queue_nachher
  1430-1432   _upload_queue_path
  1556-1560   _upload_queue_remove
  1451-1455   _upload_queue_save
  1563-1568   _upload_queue_update
 10063-10087  _upload_rest_sichern
  1574-1596   _upload_window_loop
  8073-8080   _uptime_s
 13854-13863  _url_host
  3414-3512   _url_nachschlag
   912-916    _usage_record_claude
 27207-27229  _v37_pause_source
 27171-27181  _v37_restream_restart
 27184-27204  _v37_unpause_source
  8487-8531   _verbindung_verloren
  7037-7068   _viewer_sample_loop
 10967-10970  _wants_html
  8083-8097   _warn_empty_env
 26565-26690  _watchdog_loop
 24607-24615  _wchat_thank_ok
 26886-26916  _werkzeug_wacht_loop
 19182-19220  _whisper_get_model
  8174-8182   _whisper_native_section
 18369-18375  _whisper_pool
 19314-19346  _whisper_segments
 19222-19238  _whisper_stumm
 19241-19311  _whisper_transcribe
 14327-14484  _write_restream_overlay
 14289-14324  _write_restream_overlay_async
 25247-25346  _youtube_api_chat_loop
 21592-21695  _youtube_api_status
 21698-21765  _youtube_channel_status
 25349-25513  _youtube_chat_loop
 24143-24168  _youtube_clip_versuchen
 24467-24480  _youtube_restream_autoconfig
 24483-24507  _youtube_restream_autoconfig_inner
 24574-24602  _youtube_send
 21833-21874  _youtube_set_channel
 24510-24544  _yt_access_token
 24547-24562  _yt_live_chat_id
 24570-24571  _yt_sendrate_cfg
 25226-25241  _yt_timeout
  3189-3190   _ytdlp_detect_available
  3205-3207   _ytdlp_einzeln
  3192-3203   _ytdlp_note_result
 13088-13090  _zombie_child_count
 26396-26409  _zustand_kennzahlen
  7949-7973   about
  4543-4547   add_ai_log_entry
  4460-4463   add_archive_entry
  5185-5187   add_archive_rule
  4925-4996   add_recording
  4607-4624   add_tracking
  6427-6460   ai
  4145-4231   ai_chat
  4265-4275   ai_history_append
  4277-4282   ai_history_clear
  4254-4263   ai_history_load
  4239-4252   ai_rate_limit_check
  6489-6497   aireset
 18711-18730  azrael_chat
 25518-25640  brain_cmd
  3757-3762   build_recording_cmd
  4627-4630   bulk_add_trackings
  7316-7375   bulkadd
  9356-9472   check_all_trackings
  4679-4691   claim_live_transition
 17541-18301  class KickModerator
 15329-17288  class RestreamManager
  4845-4846   class _AufnahmeLockVerloren
  8423-8484   class _KickClusterSuche
 11969-12011  classify_proxy_anonymity
  6535-6734   cleanup
  5475-5481   cleanup_old_recordings
  4870-4877   clear_recording
 24171-24192  clip_moment
  5137-5140   compute_storage_forecast
  7438-7514   cookies_cmd
  7517-7560   cookies_datei_cmd
  4598-4604   count_trackings_for_chat
  4530-4541   decide_preferred_recorder
  4470-4473   delete_archive_entry
  5189-5191   delete_archive_rule
  5964-6111   diag
 25752-25813  einnahmen_cmd
  5131-5134   find_recordings_by_fingerprint
  4491-4507   finish_recording_attempt
  4651-4653   get_all_active_trackings
  4558-4560   get_all_checks
  4998-5001   get_all_recordings
  5080-5082   get_all_tags_with_counts
  5108-5111   get_annotations_for_recording
  4465-4468   get_archive_entry
  5101-5104   get_bookmarked_recordings
  2318-2323   get_cookie_health
  5068-5074   get_event_log
  4514-4528   get_last_recording_attempt
  3515-3557   get_live_status
  5414-5417   get_manual_recordings
  5116-5119   get_or_compute_inspect_sync
  5516-5519   get_outcome_breakdown
  5087-5090   get_priority_poll_interval
  4509-4512   get_recent_recording_attempts
  5003-5006   get_recording_by_id
  5094-5097   get_recording_note
  3928-3957   get_redis
  4587-4590   get_stats
  5469-5473   get_storage_stats
  5209-5211   get_tiktok_status_distribution
  4693-4702   get_tracking_state
  4648-4649   get_trackings_for_group
  5430-5433   get_trash_recordings
 10151-10618  handle_recording_finished
 25862-25867  hilfe_cmd
  4350-4415   init_db
  5181-5183   list_archive_rules
  5749-5787   live
  8661-8691   live_check_worker
  4012-4055   llm_chat
  4078-4109   llm_chat_sync
  4063-4075   llm_list_models
  5027-5060   log_event
  1932-1965   log_recording_failure
  7710-7759   logs_cmd
 27701-27980  main
  6463-6486   on_ai_media
  7836-7862   on_ai_reply
  7917-7946   on_azrael_mention
  7978-8008   on_callback
  9738-9756   on_chat_migration
  7871-7884   on_link_video
 18736-18841  oracle_handle
  7599-7602   pause_tracking
  5529-5534   profile_keyboard
  5702-5746   quelle
  7661-7707   quota
  9135-9209   reaper_loop
  5205-5207   record_tiktok_status
  6502-6532   recstatus
  3959-3967   redis_get_json
  3970-3976   redis_set_json
 25889-25899  report_cmd
 12014-12016  report_proxy_result
  2597-2639   resolve_tiktok_live_stream
  5425-5428   restore_recording
  7605-7608   resume_tracking
  5194-5199   run_archive_rules
 25902-26174  run_bot
 12940-13034  run_flask
  5169-5172   sample_bandwidth_for_active
  4550-4556   save_tiktok_check
  4849-4868   set_recording_file
  4656-4660   set_tracking_paused
  5420-5423   soft_delete_recording
 25847-25859  spenden_cmd
  9762-9773   split_and_send_video
  5612-5654   start
  4475-4489   start_recording_attempt
  6737-6775   stats
  5359-5412   stop_manual_recording
  7611-7658   stoprec
  6961-6969   summary_cmd
  7762-7833   sysres
  6113-6257   teststream
  5656-5697   tiktok
  7378-7435   topusers
  5824-5881   track
  5789-5821   track_exact
  5895-5962   tracklist
  5243-5357   trigger_manual_recording
  4781-4816   try_acquire_recording_lock
  5436-5438   universal_search
 25816-25844  unpause_cmd
  5883-5893   untrack
 25643-25749  update_cmd
  5126-5129   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, host_ist_lokal, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, uebernehmen, zusammenfuehren
cookies.py             configure, gesundheit, hat_login, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, mariadb_lage, set_pool, treiber_fehler, treiber_wunsch, vorrat_groesse, vorrat_lage, vorrat_leeren
dcspar.py              anzeige, client_optionen, puffer
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     an, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, source_allowed, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
httpsitzung.py         schliessen, sitzung, teilen
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler, lage, teilen
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
piperarbeiter.py       main
piperdienst.py         an, beenden, lage, sprechen
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
pruefschlange.py       erledigt, mit_frist, vorgemerkt, vormerken, zuruecksetzen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
raumkennung.py         grund, gueltig
raumsperre.py          deuten, faellig, lage, merken, snapshot, text, vergessen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        ausnahme_text, class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
sitzungsschluessel.py  laden, pin_schluessel
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, faellig, gleicher, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
werkzeugpfad.py        alter_tage, befund, lage, nachahmen_aus, pruefen, voranstellen
whispercfg.py          bedarf_mb, benutzt, entladen_wenn_leer, frei_mb, gebrauch, geladen, leerlauf_s, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlparbeiter.py       main
ytdlpdienst.py         alle_beenden, anzahl, ausfuehren, laeufe_max, lage
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
zeitglaetter.py        ausdruck, bsf_args, filter_text, verfuegbar
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime, ohne_denkblock
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler, frische_intervalle
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
