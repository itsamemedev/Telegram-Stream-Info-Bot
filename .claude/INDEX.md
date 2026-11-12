# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11135  GET              /                                                dashboard
 13192  GET              /api/abo/status                                  api_abo_status
 13146  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11923  GET              /api/automation/status                           api_automation_status
 11945  POST             /api/automation/toggle                           api_automation_toggle
 21765  GET              /api/channel/categories                          api_channel_categories
 21771  POST             /api/channel/set                                 api_channel_set
 21618  GET              /api/channels/status                             api_channels_status
 21292  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21275  GET              /api/clips                                       api_clips
 21321  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21193  GET              /api/debug/threads                               api_debug_threads
 13157  GET              /api/events                                      api_events
 12636  GET              /api/events/stream                               api_events_stream
 12463  GET              /api/health                                      api_health
 21234  POST             /api/highlights/config                           api_highlights_config
 11065  POST             /api/login                                       dashboard_login_submit
 13482  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12551  GET              /api/notify/status                               api_notify_status
 12562  POST             /api/notify/test                                 api_notify_test
 13246  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13223  GET              /api/proxy/trend                                 api_proxy_trend
 21341  GET              /api/tts/<fn>                                    api_tts_file
 22115  GET              /api/upload_window                               api_upload_window
 12753  GET              /archive/<int:eid>/download                      archive_download
 12781  GET              /download/<int:recording_id>                     download
 12710  GET              /health                                          health
 21087  GET              /healthz                                         healthz
 11056  GET              /login                                           dashboard_login_page
 11090  GET              /logout                                          dashboard_logout
 11097  GET              /manifest.webmanifest                            pwa_manifest
 22088  GET              /overlay                                         overlay_page
 11121  GET              /pwa-icon-<variant>.png                          pwa_icon
 11107  GET              /sw.js                                           pwa_service_worker
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
   439  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   424  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   244  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   265  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   292  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   385  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   329  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   347  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   252  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   480  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   470  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   505  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
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
  2276  /about                  Ueber diesen Bot
   980  /ai                     
  2276  /aireset                KI-Kontext zuruecksetzen
  1395  /ask                    
  1081  /assign_role            
  1131  /ban                    
  2231  /botstats               
  2276  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2276  /bulkadd                Mehrere User auf einmal tracken · a b c
  2276  /cleanup                Alte Aufnahmen aufraeumen
  1661  /clearwarns             
  2195  /clip                   
  2180  /clipoftheweek          
  1531  /clips                  
  2276  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1036  /create_category        
  1007  /create_channel         
  1071  /create_group           
  1046  /create_role            
  1022  /create_voice           
  1272  /daily                  
  2276  /diag                   Vollstaendige Diagnose
  2276  /einnahmen              Einnahmen und Spenden
  1424  /event                  
  1466  /events                 
  1571  /follow                 
  1560  /help                   
  1121  /kick                   
  1247  /leaderboard            
  2276  /live                   Live-Status sofort pruefen · @user
  1518  /livenow                
  2276  /logs                   Letzte Fehler aus dem Log
  2276  /pause                  Tracking pausieren · @user
  1546  /post_test              
  1356  /profile                
  1153  /purge                  
  2276  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2276  /quota                  Speicher-Quota
  1234  /rank                   
  1506  /recstatus              
  1091  /remove_role            
  2276  /report                 Azrael-Sentinel-Wochenreport
   993  /restream_status        
  2276  /resume                 Tracking fortsetzen · @user
  1101  /set_channel_perms      
  1196  /setup_community        
  1213  /setup_targets          
  1492  /spenden                
  1603  /stats                  
   952  /status                 
  2276  /stoprec                Laufende Aufnahme sauber beenden · @user
  1699  /streaminfo             
  2276  /summary                Tageszusammenfassung
  2276  /sysres                 System-Ressourcen
  2276  /teststream             Recorder-Selbsttest · @user
  2276  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1141  /timeout                
  1671  /topstreamers           
  2276  /topusers               Top-Streamer nach Aufnahmen
   882  /track                  
  2276  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   965  /tracklist              
  1585  /unfollow               
  2276  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   914  /untrack                
  1624  /warn                   
  1647  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2443  on_member_join
  2400  on_message
  2297  on_raw_reaction_add
  2478  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1776-1827   _award_xp
   536-563    _bereich_umziehen
   483-493    _clip_kopieren
  1998-2027   _clip_week_leader
  2051-2065   _clipoftheweek_loop
  2595-2657   _community_events_loop
  1733-1755   _dc_client
  1758-1767   _dc_offen
  2697-2732   _disc_automod_check
   409-414    _disc_sprache_setzen
  1830-1878   _discord_ai_automod
   685-724    _discord_automod
  1881-1901   _discord_azrael_reply
  2068-2554   _discord_run_once
   244-302    _discord_start
   305-359    _ensure_discord_invite
  2560-2592   _ensure_error_channel
   430-443    _ensure_rank_roles
   845-859    _ensure_team_roles
  2660-2690   _error_channel_loop
   734-738    _guard
   654-682    _handle_voice_ai
   417-427    _is_admin
   508-533    _link_video
  1946-1957   _liveboard_loop
   741-774    _on_level_up
   650-651    _par_chat_id
  2030-2048   _post_clip_of_week
  1960-1978   _post_weekly_digest
   446-472    _provision_base_channels
  1498-1592   _reg_betrieb
  1167-1261   _reg_community_setup
  1264-1345   _reg_daily_profil
  1388-1485   _reg_frage_events
   939-995    _reg_info
  1113-1164   _reg_moderation
  1348-1385   _reg_profil
  1062-1110   _reg_rollen
   998-1059   _reg_server
  1488-1495   _reg_spenden
  1595-1682   _reg_streamer
  1685-1730   _reg_system
   873-936    _reg_tracking
   809-842    _run_tg_handler
   637-647    _tracked_usernames
   161-223    _uebernehmen
   496-505    _umzugsmarken
  1910-1943   _update_liveboard
  1981-1995   _weekly_digest_loop
   475-480    _ziel_guild
   566-608    _ziele_abgleichen
   617-634    _ziele_sync_loop
   611-614    _ziele_takt_min
   226-229    starte
```

## Top-Level-Symbole in bot.py (603 Funktionen, 4 Klassen)

```
 27234-27256  _abbruch_datenbank_unlesbar
  2830-2831   _abo_key
  2851-2869   _abo_probe_dump
 27352-27368  _abschied_wachen
 27371-27389  _abschluss
 17355-17362  _ad_allowlist
 18517-18523  _agent_for
 18526-18542  _ai_telemetry
 19039-19057  _alert
 22983-23033  _alert_monitor_loop
 19733-19790  _alte_beilagen_einsammeln
 23415-23477  _announce_loop
  3730-3740   _anthropic_key
  3747-3749   _anthropic_model
 10624-10627  _arg_int
  2822-2827   _as_dict
 26920-26929  _async_exc_handler
 19227-19249  _audio_tap_cmd
 20253-20312  _audio_tap_melden
 19263-19287  _audio_tap_sammler
  9970-10007  _aufnahme_beim_stopp_sichern
 19675-19696  _aufnahme_chat_ausklang
 19659-19672  _aufnahme_chat_beginnen
 19818-19839  _aufnahme_chat_dienst
 20012-20065  _aufnahme_chat_einarbeiten
 19654-19656  _aufnahme_chat_modus
 19842-19891  _aufnahme_chat_nachtrag
 19699-19730  _aufnahme_chat_vormerken
 19809-19815  _aufnahme_chat_wecken
 26114-26116  _aufnahme_deckel
 19894-19915  _aufnahme_fertigmachen
 23652-23705  _aufnahme_nach_discord
 10010-10028  _aufnahme_platz_frei
  9913-9940   _aufnahme_verteilen
 27316-27336  _aufnahmen_abschliessen
 27259-27313  _aufraeumen
 10898-10967  _auth_cookie
 10854-10894  _auth_guard
  2057-2062   _auto_on
 20939-20957  _auto_restream_loop
 14827-14869  _avatar_frames_laden
 17405-17418  _azrael_brain_kontext
 24611-24626  _azrael_broadcast_reply
 24511-24533  _azrael_chat_reply
 24483-24508  _azrael_chat_should_reply
 24539-24541  _azrael_gate_cfg
 18547-18561  _azrael_live_state
 22001-22015  _azrael_overlay_state
 18921-18975  _azrael_proactive_loop
 18365-18421  _azrael_reaction_to_chats
 24544-24551  _azrael_reply_all_chats
 24470-24480  _azrael_self_names
 24579-24608  _azrael_send_to
 14788-14824  _azrael_spricht
 15135-15148  _azrael_stimme_stumm
 18567-18588  _azrael_system
 23117-23120  _backup_active
 23198-23211  _backup_loop
  5488-5511   _betreiber_pruefen
 26203-26207  _betrieb
 26993-27002  _brain_crowdsec_snap
 27161-27164  _brain_db_health
 22904-22913  _brain_growth_loop
 11314-11341  _brain_growth_snapshot
  2741-2775   _brain_hint_delay
 27065-27100  _brain_moderation_snap
  6762-6790   _brain_notify
 27167-27189  _brain_recording_snap
 27005-27062  _brain_restream_health
 27192-27205  _brain_tiktok_status_snap
 12615-12632  _browser_push
  6802-6889   _build_daily_summary
 15182-15186  _build_restream_cmd
  5514-5541   _can_stop_tracking
  2170-2192   _capture_set_cookies
 13300-13303  _cfg_get
 13306-13308  _cfg_set
 21726-21761  _channel_set_all
 13879-13882  _chat_connected
 13885-13901  _chat_disconnected
 19803-19806  _chat_einarbeiten_async
  9408-9438   _chat_is_forum
 19623-19648  _chat_listener_abbauen
  9580-9615   _chat_migriert
  9618-9619   _chat_migriert_async
 13921-13923  _chat_sanitize
 13864-13876  _chat_stat
 13904-13907  _chat_stats_snapshot
  4053-4065   _check_ai_models_sync
 11596-11639  _classify_pool_anonymity
 11642-11659  _classify_pool_anonymity_bg
   906-928    _claude_chat_sync_metered
 10656-10662  _client_ip
 24110-24124  _clip_chat_ass
 23561-23595  _clip_prune
 23598-23608  _clip_recfile_for
 24030-24098  _clip_schneiden
 24127-24133  _clip_should_velocity
 23708-23793  _clip_to_discord
 19983-19988  _clips_abwarten
  3934-3943   _close_ai_session
 24657-24672  _cohost_broadcast
 24642-24643  _cohost_cfg
 24698-24710  _cohost_fire_highlight
 24646-24654  _cohost_gate
 24675-24695  _cohost_highlight
 11244-11246  _conv_messages
  7186-7247   _cookie_alarm_loop
  2260-2261   _cookie_autofetch_info
  2244-2248   _cookie_autorefresh_info
 26627-26649  _cookie_bezug_loop
 26652-26677  _cookie_bezug_runde
  2147-2151   _cookie_header
 10665-10670  _cookie_sicher
  2273-2287   _cookies_selbst_holen
  4274-4276   _create_index_safe
 22447-22561  _crowdsec_status
 22393-22444  _crowdsec_via_lapi
 22297-22315  _cscli_bin
 22324-22337  _cscli_path
  7070-7097   _daily_summary_loop
 22355-22372  _darf_journal_lesen
  3255-3280   _darf_ytdlp_nachschlagen
 12796-12817  _dashboard_adresse
 10685-10689  _dashboard_hostnamen
  1509-1539   _dashboard_trackings_umziehen
 24101-24107  _datei_weg
 22957-22980  _db_maintenance_loop
  7020-7067   _db_vacuum_loop
 17378-17402  _detect_foreign_ad
  1737-1748   _diag_path_owner
 18826-18871  _director_finalize
 20242-20249  _director_for
 18775-18823  _director_mark
 23943-23946  _disc_state_get
 23949-23956  _disc_state_set
 22885-22894  _discord_bot_starten
 22848-22859  _discord_einladung_merken
 22897-22901  _discord_invite
 22862-22882  _discord_kontext
 23904-23940  _discord_live_thread
 18978-18990  _discord_notify
 22820-22845  _discord_ops_alert
 23804-23900  _discord_post_user
 23480-23486  _discord_stop
  7100-7181   _disk_alarm_loop
 26498-26549  _disk_autoclean
 26775-26788  _disk_guard_loop
 14766-14773  _drossel_hoeher
 14762-14763  _drossel_stufe
 14776-14784  _drossel_zuruecksetzen
 12973-12975  _dump_all_threads
 26210-26224  _einstellungen_startzeile
 11522-11585  _enrich_proxies_with_geo
  2316-2377   _ensure_cookie_file_netscape
  9509-9512   _ensure_notify_topic
 11766-11803  _ensure_proxy_ready
  9448-9471   _ensure_topic
   747-749    _env_int
   752-754    _env_int_range
 19023-19036  _event_webhook
 13647-13660  _evolution_loop
  6203-6237   _extract_file_payload
  2449-2451   _extract_urls_from_streamurl_node
 22340-22347  _f2b_sudo_hint
  1495-1506   _fanout_ziele
 27392-27455  _fatal_vom_botteil
 26119-26134  _fd_grenze_anheben
  4948-4958   _fehler_text
 11423-11441  _fetch_proxy_list
 19592-19620  _fetch_tiktok_room_id
   832-835    _ff_cmd
 19996-20009  _ffprobe_masse
 14710-14726  _fifo_schreiber_wecken
 14520-14525  _find_chromium
  3650-3652   _find_external_recorder
  2454-2456   _find_stream_urls
 13351-13376  _fire_webhooks
  8070-8080   _fork_safe
   939-952    _freeai_chat_sync_metered
 22386-22390  _geo_lookup_ips
  3922-3931   _get_ai_session
  7898-7938   _get_live_info
  3106-3113   _get_resolve_semaphore
  8597-9017   _handle_single_tracking
 26319-26321  _hb
 26324-26341  _hb_while
 10971-10988  _herkunft_guard
 13935-13937  _highlight_cfg
 13940-13969  _highlight_observe
 14571-14579  _htmlov_bild_schreiben
 14549-14568  _htmlov_dauerbrowser
 14528-14546  _htmlov_screenshot_cmd
 19289-19299  _httpx_proxy
 13384-13396  _in_quiet_hours
 27220-27231  _init_db_oder_abbruch
 28042-28073  _install_fast_eventloop
 10519-10573  _install_fast_json
 12978-12994  _install_faulthandler
 20990-20999  _intel_ensure_schema
 21042-21077  _intel_index_loop
 21011-21026  _intel_index_one
 21002-21008  _intel_semantic
  5473-5486   _is_authorized
  8423-8444   _is_dead
  2439-2441   _is_hevc
 22375-22377  _is_private_ip
  1956-1963   _is_process_running
  6792-6799   _is_quiet_hours
  1397-1406   _is_upload_window
  4813-4828   _iso
 10673-10682  _ist_lokal
 10608-10621  _json_error_handler
  7014-7015   _kick_broadcaster_id
  8298-8305   _kick_cluster_gefunden
  8233-8295   _kick_cluster_weiter
  6926-6968   _kick_follower_count
  6910-6913   _kick_slug
 12428-12435  _kick_user_token
  8203-8230   _kick_ws_pause
 27208-27217  _kickmod_boot
  4358-4361   _kind_from_filename
 26593-26596  _lagebild_discord_aufnahme
 26606-26610  _lagebild_kick_chat
 26599-26603  _lagebild_overlay
 26613-26615  _lagebild_spendenziel
 26580-26590  _lagebild_upload
 13413-13415  _latest_popularity
  1893-1902   _laufstand
 26735-26772  _laufstand_loop
 26243-26281  _leistung_erheben
  7772-7799   _link_video_senden
  8584-8595   _live_check_frist_melden
 20648-20697  _live_react_loop
 20315-20637  _live_react_worker
  3498-3612   _live_status_aufloesen
 18424-18435  _live_transcript_push
 20639-20646  _live_users
 18874-18918  _living_title_loop
 23123-23195  _local_backup_scan
  4753-4776   _lock_update
 10590-10604  _log_5xx
 26284-26316  _log_schleuse_pruefen
   822-829    _log_sicher
 15194-15206  _looks_like_codec_err
 15189-15191  _looks_like_source_expired
  8121-8151   _loop_fehler
 12998-13007  _loop_heartbeat
 26025-26058  _loop_lag_monitor
 26072-26092  _loop_stockung_melden
 26095-26105  _loop_takt_starten
 13010-13083  _loop_watchdog_thread
 18301-18318  _loyalty_add
 18292-18298  _loyalty_get
 18321-18329  _loyalty_top
  5155-5174   _manual_status
  8446-8447   _mark_dead
 12042-12058  _marketing_loop
 24558-24576  _maybe_handle_command
 26874-26898  _maybe_hype_clip
 23530-23558  _meme_klassifizieren
 19918-19980  _meme_zusammenschnitt
  4261-4266   _migrate_columns
 24840-24851  _mod_is_exempt
 24854-24859  _mod_warn_first
 24862-24865  _mod_warn_text
 13704-13723  _modlog
 13687-13701  _modlog_schreiben
  1093-1095   _multistream_targets
  3283-3319   _nachschlag_ytdlp
  8083-8084   _nc_create_subprocess_exec
  8087-8088   _nc_create_subprocess_shell
 12365-12382  _news_loop
 13746-13748  _normalize_ingest
  2672-2689   _note_check_duration
  9503-9506   _notify_topic_name
  2876-2882   _offline_ergebnis
  3322-3345   _ohne_url_melden
 18450-18458  _oracle_memories
 18724-18758  _oracle_memorize
 18461-18474  _oracle_persona
 18443-18447  _oracle_recent_text
 14144-14145  _ov_atomic_write
 14135-14137  _ov_bar
 17281-17293  _ov_clip_text
 14140-14141  _ov_oneline
 22052-22081  _overlay_push
 14474-14517  _overlay_render_size
 13815-13819  _overlay_session_reset
 22017-22019  _overlay_src_ok
 14154-14166  _overlay_takt
 17365-17375  _own_invites
 14469-14471  _parse_size
 22569-22649  _parse_ssh_attacks
  7448-7481   _pause_resume_cmd
  2198-2242   _persist_refreshed_cookies
  2101-2133   _pick_checked_pull_proxy
 10739-10754  _pin_auth_value
 10843-10844  _pin_clear_fail
 10807-10810  _pin_global_gesperrt
 10760-10771  _pin_hmac_schluessel
 10813-10820  _pin_locked
 10823-10840  _pin_note_fail
 10774-10795  _pin_ok
 21859-21884  _piper_pick_model
 21944-21995  _piper_say
 13313-13348  _post_json_threaded
 14448-14466  _probe_video_size
  1984-2001   _proc_is_recorder
 11735-11763  _proxy_pool_refresh_loop
  2067-2098   _proxy_report_recording
  9156-9237   _pruef_runde
  9115-9153   _pruefstand_melden
 26154-26165  _pruefung_verworfen
 12963-12965  _prune_stall_dumps
 12112-12284  _public_stats
  2264-2270   _pull_proxy_still
 18994-19020  _push_notify
 11035-11037  _pwa_dir
 11492-11507  _quick_validate_proxy
 13379-13381  _quiet_hours_config
 11000-11033  _rate_guard
 18262-18268  _react_warn
  7985-8024   _reap_proc
 10692-10708  _rebinding_melden
  9843-9910   _rec_auto_abschalten
  9790-9840   _rec_frueh_getrennt
  9659-9735   _rec_kategorie_melden
  9738-9787   _rec_totstreak_fortschreiben
  2712-2734   _record_check_outcome
   817-819    _redact_stream_urls
 11662-11732  _refresh_proxy_pool
  2489-2580   _resolve_via_html
  2885-3083   _resolve_via_webcast_api_v2
  3146-3231   _resolve_via_ytdlp
 24167-24296  _resolve_youtube_ingest
  2465-2486   _resolver_stumm
 13798-13809  _restream_active_sources
 14872-14999  _restream_avatar_feeder_start
 15002-15012  _restream_avatar_feeder_stop
 20068-20206  _restream_chat_guardian
 13972-14044  _restream_chat_push
 14121-14130  _restream_chat_push_async
 27103-27158  _restream_durchreicher
 14582-14707  _restream_html_overlay_start
 14729-14749  _restream_html_overlay_stop
 13757-13780  _restream_overlay_files
 20701-20733  _restream_platform_state
 20901-20936  _restream_resume_after_restart
 14075-14092  _restream_soll_schreiben
 14095-14118  _restream_status_schreiben
 15060-15132  _restream_tts_enqueue_wav
 14410-14442  _restream_tts_feeder
 14407-14408  _restream_tts_fifo_path
 15015-15042  _restream_tts_start
 15044-15058  _restream_tts_stop
 20739-20898  _restream_verify_loop
 23088-23100  _retention_loop
 23082-23085  _retention_scan
  2833-2835   _room_is_abo
  6241-6358   _run_ai_call
 13106-13119  _run_async_from_flask
 22380-22383  _run_priv
 28030-28038  _run_selfcheck_and_exit
 23103-23114  _s3_client
  8473-8543   _safe_send
  5081-5097   _sample_net_throughput
  2778-2808   _schedule_next_check
 23036-23079  _scheduler_loop
  4269-4271   _schema_pk
 13123-13128  _scraper_session
 24868-24907  _screen_full
 12479-12516  _sec_headers
  2444-2446   _select_stream_from_data_section
 27747-28027  _selfcheck
  9515-9549   _send_live_notice
  1420-1424   _should_defer_upload
 23611-23649  _shrink_for_discord
 11040-11052  _sicheres_ziel
 22916-22954  _sicherheits_erinnerung_loop
 26795-26812  _sign_health_check
 26815-26834  _sign_health_loop
  4831-4856   _sitzung_bestimmen
  8100-8111   _spawn
 28461-28491  _spawn_from_flask
 26168-26174  _speicher_maps
 26177-26192  _speicher_pflegen
 19301-19589  _start_chat_listener
 26137-26151  _start_gesperrt
 13086-13103  _start_loop_watchdog
 12311-12360  _stats_loop
 12290-12293  _stats_output_path
 12296-12308  _stats_write
 21896-21910  _stimme_saubern
 21917-21941  _stimme_schon_gesagt
  9096-9112   _storage_cleanup_loop
 26854-26861  _story_for
  3675-3681   _stream_url_expiry
  3683-3688   _stream_url_ttl
 17328-17335  _streamer_persona_get
 23220-23372  _system_backup
 23381-23411  _system_backup_loop
 12923-12941  _task_auf_bot_schleife
 25705-25721  _telegram_befehlsmenue
  8154-8200   _telegram_polling_fehler
  1465-1492   _telegram_ziele
 11444-11483  _test_proxy
 11990-12006  _testpush_resolve_live
 19991-19993  _text_schreiben
  9567-9577   _tg_migriert_laden
  9563-9564   _tg_migriert_pfad
  8449-8470   _tg_sprache_setzen
  9377-9387   _tg_topics_load_into_mem
  9374-9375   _tg_topics_path
  9389-9396   _tg_topics_save
 10711-10721  _token_ok
  9474-9490   _topic_anlegen
  9399-9406   _topic_forget
 13399-13410  _tracking_max_duration
  4566-4580   _tracking_remove_cleanup
  4597-4609   _tracking_resume_cleanup
  1795-1818   _try_attach_file_handler
 21886-21894  _tts_cleanup
 11966-11970  _tunnel_effective
 26552-26572  _tunnel_lage
 26680-26732  _tunnel_wacht_loop
 21385-21438  _twitch_channel_status
 24910-25058  _twitch_chat_loop
 23962-23975  _twitch_clip_versuchen
 24721-24827  _twitch_eventsub_loop
  1585-1620   _upload_queue_abarbeiten
  1443-1463   _upload_queue_add
  1556-1558   _upload_queue_count
  1426-1435   _upload_queue_load
  1623-1645   _upload_queue_nachher
  1416-1418   _upload_queue_path
  1542-1546   _upload_queue_remove
  1437-1441   _upload_queue_save
  1549-1554   _upload_queue_update
  9943-9967   _upload_rest_sichern
  1560-1582   _upload_window_loop
  7958-7965   _uptime_s
 13734-13743  _url_host
  3348-3446   _url_nachschlag
   899-903    _usage_record_claude
 26968-26990  _v37_pause_source
 26932-26942  _v37_restream_restart
 26945-26965  _v37_unpause_source
  8372-8416   _verbindung_verloren
  6971-7002   _viewer_sample_loop
 10847-10850  _wants_html
  7968-7982   _warn_empty_env
 26362-26484  _watchdog_loop
 24442-24450  _wchat_thank_ok
 19062-19099  _whisper_get_model
  8059-8067   _whisper_native_section
 18249-18255  _whisper_pool
 19193-19225  _whisper_segments
 19101-19117  _whisper_stumm
 19120-19190  _whisper_transcribe
 14207-14364  _write_restream_overlay
 14169-14204  _write_restream_overlay_async
 25082-25181  _youtube_api_chat_loop
 21441-21544  _youtube_api_status
 21547-21614  _youtube_channel_status
 25184-25348  _youtube_chat_loop
 23978-24003  _youtube_clip_versuchen
 24302-24315  _youtube_restream_autoconfig
 24318-24342  _youtube_restream_autoconfig_inner
 24409-24437  _youtube_send
 21682-21723  _youtube_set_channel
 24345-24379  _yt_access_token
 24382-24397  _yt_live_chat_id
 24405-24406  _yt_sendrate_cfg
 25061-25076  _yt_timeout
  3130-3131   _ytdlp_detect_available
  3133-3144   _ytdlp_note_result
 12968-12970  _zombie_child_count
 26227-26240  _zustand_kennzahlen
  7834-7858   about
  4477-4481   add_ai_log_entry
  4394-4397   add_archive_entry
  5119-5121   add_archive_rule
  4859-4930   add_recording
  4541-4558   add_tracking
  6361-6394   ai
  4079-4165   ai_chat
  4199-4209   ai_history_append
  4211-4216   ai_history_clear
  4188-4197   ai_history_load
  4173-4186   ai_rate_limit_check
  6423-6431   aireset
 18591-18610  azrael_chat
 25353-25475  brain_cmd
  3691-3696   build_recording_cmd
  4561-4564   bulk_add_trackings
  7250-7309   bulkadd
  9240-9356   check_all_trackings
  4613-4625   claim_live_transition
 17421-18181  class KickModerator
 15209-17168  class RestreamManager
  4779-4780   class _AufnahmeLockVerloren
  8308-8369   class _KickClusterSuche
 11849-11891  classify_proxy_anonymity
  6469-6668   cleanup
  5409-5415   cleanup_old_recordings
  4804-4811   clear_recording
 24006-24027  clip_moment
  5071-5074   compute_storage_forecast
  7372-7445   cookies_cmd
  4532-4538   count_trackings_for_chat
  4464-4475   decide_preferred_recorder
  4404-4407   delete_archive_entry
  5123-5125   delete_archive_rule
  5898-6045   diag
 25587-25648  einnahmen_cmd
  5065-5068   find_recordings_by_fingerprint
  4425-4441   finish_recording_attempt
  4585-4587   get_all_active_trackings
  4492-4494   get_all_checks
  4932-4935   get_all_recordings
  5014-5016   get_all_tags_with_counts
  5042-5045   get_annotations_for_recording
  4399-4402   get_archive_entry
  5035-5038   get_bookmarked_recordings
  2304-2309   get_cookie_health
  5002-5008   get_event_log
  4448-4462   get_last_recording_attempt
  3449-3491   get_live_status
  5348-5351   get_manual_recordings
  5050-5053   get_or_compute_inspect_sync
  5450-5453   get_outcome_breakdown
  5021-5024   get_priority_poll_interval
  4443-4446   get_recent_recording_attempts
  4937-4940   get_recording_by_id
  5028-5031   get_recording_note
  3862-3891   get_redis
  4521-4524   get_stats
  5403-5407   get_storage_stats
  5143-5145   get_tiktok_status_distribution
  4627-4636   get_tracking_state
  4582-4583   get_trackings_for_group
  5364-5367   get_trash_recordings
 10031-10498  handle_recording_finished
 25697-25702  hilfe_cmd
  4284-4349   init_db
  5115-5117   list_archive_rules
  5683-5721   live
  8546-8576   live_check_worker
  3946-3989   llm_chat
  4012-4043   llm_chat_sync
  3997-4009   llm_list_models
  4961-4994   log_event
  1918-1951   log_recording_failure
  7595-7644   logs_cmd
 27458-27737  main
  6397-6420   on_ai_media
  7721-7747   on_ai_reply
  7802-7831   on_azrael_mention
  7863-7893   on_callback
  9622-9640   on_chat_migration
  7756-7769   on_link_video
 18616-18721  oracle_handle
  7484-7487   pause_tracking
  5463-5468   profile_keyboard
  5636-5680   quelle
  7546-7592   quota
  9019-9093   reaper_loop
  5139-5141   record_tiktok_status
  6436-6466   recstatus
  3893-3901   redis_get_json
  3904-3910   redis_set_json
 25724-25734  report_cmd
 11894-11896  report_proxy_result
  2583-2625   resolve_tiktok_live_stream
  5359-5362   restore_recording
  7490-7493   resume_tracking
  5128-5133   run_archive_rules
 25737-26005  run_bot
 12820-12914  run_flask
  5103-5106   sample_bandwidth_for_active
  4484-4490   save_tiktok_check
  4783-4802   set_recording_file
  4590-4594   set_tracking_paused
  5354-5357   soft_delete_recording
 25682-25694  spenden_cmd
  9646-9657   split_and_send_video
  5546-5588   start
  4409-4423   start_recording_attempt
  6671-6709   stats
  5293-5346   stop_manual_recording
  7496-7543   stoprec
  6895-6903   summary_cmd
  7647-7718   sysres
  6047-6191   teststream
  5590-5631   tiktok
  7312-7369   topusers
  5758-5815   track
  5723-5755   track_exact
  5829-5896   tracklist
  5177-5291   trigger_manual_recording
  4715-4750   try_acquire_recording_lock
  5370-5372   universal_search
 25651-25679  unpause_cmd
  5817-5827   untrack
 25478-25584  update_cmd
  5060-5063   update_recording_fingerprint
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
cookieholen.py         aktualisiere, aus_browser, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
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
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
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
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
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
whispercfg.py          bedarf_mb, frei_mb, geladen, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
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
