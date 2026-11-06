# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10299  GET              /                                                dashboard
 12354  GET              /api/abo/status                                  api_abo_status
 12308  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11087  GET              /api/automation/status                           api_automation_status
 11109  POST             /api/automation/toggle                           api_automation_toggle
 19991  GET              /api/channel/categories                          api_channel_categories
 19997  POST             /api/channel/set                                 api_channel_set
 19844  GET              /api/channels/status                             api_channels_status
 19518  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19501  GET              /api/clips                                       api_clips
 19547  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19419  GET              /api/debug/threads                               api_debug_threads
 12319  GET              /api/events                                      api_events
 11798  GET              /api/events/stream                               api_events_stream
 11625  GET              /api/health                                      api_health
 19460  POST             /api/highlights/config                           api_highlights_config
 10229  POST             /api/login                                       dashboard_login_submit
 12644  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11713  GET              /api/notify/status                               api_notify_status
 11724  POST             /api/notify/test                                 api_notify_test
 12408  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12385  GET              /api/proxy/trend                                 api_proxy_trend
 19567  GET              /api/tts/<fn>                                    api_tts_file
 20344  GET              /api/upload_window                               api_upload_window
 11915  GET              /archive/<int:eid>/download                      archive_download
 11943  GET              /download/<int:recording_id>                     download
 11872  GET              /health                                          health
 19328  GET              /healthz                                         healthz
 10220  GET              /login                                           dashboard_login_page
 10254  GET              /logout                                          dashboard_logout
 10261  GET              /manifest.webmanifest                            pwa_manifest
 20317  GET              /overlay                                         overlay_page
 10285  GET              /pwa-icon-<variant>.png                          pwa_icon
 10271  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
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
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
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
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
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
   202  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   222  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   249  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
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
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
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
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
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
   509  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   526  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   578  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   600  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   539  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   565  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
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
   239  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   460  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   489  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   409  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   422  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   518  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   395  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   270  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   315  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   339  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   326  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   166  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   284  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   136  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   376  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   431  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
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

## Discord-Slash-Commands in discordbot.py (66)

```
  2171  /about                  Ueber diesen Bot
   890  /ai                     
  2171  /aireset                KI-Kontext zuruecksetzen
  1302  /ask                    
   991  /assign_role            
  1041  /ban                    
  2126  /botstats               
  2171  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2171  /bulkadd                Mehrere User auf einmal tracken · a b c
  2171  /cleanup                Alte Aufnahmen aufraeumen
  1557  /clearwarns             
  2090  /clip                   
  2075  /clipoftheweek          
  1428  /clips                  
  2171  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   946  /create_category        
   917  /create_channel         
   981  /create_group           
   956  /create_role            
   932  /create_voice           
  1180  /daily                  
  2171  /diag                   Vollstaendige Diagnose
  2171  /einnahmen              Einnahmen und Spenden
  1331  /event                  
  1373  /events                 
  1467  /follow                 
  1456  /help                   
  1031  /kick                   
  1155  /leaderboard            
  2171  /live                   Live-Status sofort pruefen · @user
  1415  /livenow                
  2171  /logs                   Letzte Fehler aus dem Log
  2171  /pause                  Tracking pausieren · @user
  1443  /post_test              
  1263  /profile                
  1063  /purge                  
  2171  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2171  /quota                  Speicher-Quota
  1142  /rank                   
  1403  /recstatus              
  1001  /remove_role            
  2171  /report                 Azrael-Sentinel-Wochenreport
   903  /restream_status        
  2171  /resume                 Tracking fortsetzen · @user
  1011  /set_channel_perms      
  1106  /setup_community        
  1123  /setup_targets          
  1499  /stats                  
   862  /status                 
  2171  /stoprec                Laufende Aufnahme sauber beenden · @user
  1595  /streaminfo             
  2171  /summary                Tageszusammenfassung
  2171  /sysres                 System-Ressourcen
  2171  /teststream             Recorder-Selbsttest · @user
  2171  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1051  /timeout                
  1567  /topstreamers           
  2171  /topusers               Top-Streamer nach Aufnahmen
   792  /track                  
  2171  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   875  /tracklist              
  1481  /unfollow               
  2171  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   824  /untrack                
  1520  /warn                   
  1543  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2329  on_member_join
  2291  on_message
  2192  on_raw_reaction_add
  2364  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-476    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (51 Funktionen)

```
   489-494    _alle_getrackten
  1672-1723   _award_xp
  1894-1923   _clip_week_leader
  1947-1961   _clipoftheweek_loop
  2481-2543   _community_events_loop
  1629-1651   _dc_client
  1654-1663   _dc_offen
  2583-2618   _disc_automod_check
   404-409    _disc_sprache_setzen
  1726-1774   _discord_ai_automod
   613-652    _discord_automod
  1777-1797   _discord_azrael_reply
  1964-2440   _discord_run_once
   239-297    _discord_start
   300-354    _ensure_discord_invite
  2446-2478   _ensure_error_channel
   425-438    _ensure_rank_roles
   755-769    _ensure_team_roles
  2546-2576   _error_channel_loop
   662-666    _guard
   582-610    _handle_voice_ai
   412-422    _is_admin
  1842-1853   _liveboard_loop
   669-687    _on_level_up
   578-579    _par_chat_id
  1926-1944   _post_clip_of_week
  1856-1874   _post_weekly_digest
   441-467    _provision_base_channels
   470-486    _provision_user_channels
  1395-1488   _reg_betrieb
  1077-1169   _reg_community_setup
  1172-1252   _reg_daily_profil
  1295-1392   _reg_frage_events
   849-905    _reg_info
  1023-1074   _reg_moderation
  1255-1292   _reg_profil
   972-1020   _reg_rollen
   908-969    _reg_server
  1491-1578   _reg_streamer
  1581-1626   _reg_system
   783-846    _reg_tracking
   722-752    _run_tg_handler
   565-575    _tracked_usernames
   156-218    _uebernehmen
  1806-1839   _update_liveboard
  1877-1891   _weekly_digest_loop
   497-502    _ziel_guild
   505-536    _ziele_abgleichen
   545-562    _ziele_sync_loop
   539-542    _ziele_takt_min
   221-224    starte
```

## Top-Level-Symbole in bot.py (547 Funktionen, 3 Klassen)

```
 25246-25268  _abbruch_datenbank_unlesbar
  2665-2666   _abo_key
  2686-2704   _abo_probe_dump
 25364-25380  _abschied_wachen
 25383-25401  _abschluss
 16209-16216  _ad_allowlist
 17211-17217  _agent_for
 17220-17236  _ai_telemetry
 17733-17751  _alert
 21212-21262  _alert_monitor_loop
 21644-21706  _announce_loop
  3552-3562   _anthropic_key
  3569-3571   _anthropic_model
  9884-9887   _arg_int
  2657-2662   _as_dict
 24944-24953  _async_exc_handler
 17914-17936  _audio_tap_cmd
 18494-18553  _audio_tap_melden
 17950-17974  _audio_tap_sammler
  9232-9265   _aufnahme_beim_stopp_sichern
 24193-24195  _aufnahme_deckel
  9268-9286   _aufnahme_platz_frei
 25328-25348  _aufnahmen_abschliessen
 25271-25325  _aufraeumen
 10083-10152  _auth_cookie
 10041-10079  _auth_guard
  1906-1911   _auto_on
 19180-19198  _auto_restream_loop
 13886-13928  _avatar_frames_laden
 22727-22742  _azrael_broadcast_reply
 22627-22649  _azrael_chat_reply
 22599-22624  _azrael_chat_should_reply
 22655-22657  _azrael_gate_cfg
 17241-17255  _azrael_live_state
 20230-20244  _azrael_overlay_state
 17615-17669  _azrael_proactive_loop
 17059-17115  _azrael_reaction_to_chats
 22660-22667  _azrael_reply_all_chats
 22586-22596  _azrael_self_names
 22695-22724  _azrael_send_to
 13847-13883  _azrael_spricht
 14190-14203  _azrael_stimme_stumm
 17261-17282  _azrael_system
 21346-21349  _backup_active
 21427-21440  _backup_loop
 24282-24286  _betrieb
 25017-25026  _brain_crowdsec_snap
 25173-25176  _brain_db_health
 21133-21142  _brain_growth_loop
 10478-10505  _brain_growth_snapshot
  2590-2610   _brain_hint_delay
 25089-25124  _brain_moderation_snap
  6498-6526   _brain_notify
 25179-25201  _brain_recording_snap
 25029-25086  _brain_restream_health
 25204-25217  _brain_tiktok_status_snap
 11777-11794  _browser_push
  6538-6625   _build_daily_summary
 14237-14241  _build_restream_cmd
  5251-5278   _can_stop_tracking
  2019-2041   _capture_set_cookies
 12462-12465  _cfg_get
 12468-12470  _cfg_set
 19952-19987  _channel_set_all
 13045-13048  _chat_connected
 13051-13067  _chat_disconnected
  8861-8872   _chat_is_forum
 18301-18326  _chat_listener_abbauen
 13087-13089  _chat_sanitize
 13030-13042  _chat_stat
 13070-13073  _chat_stats_snapshot
  3870-3882   _check_ai_models_sync
 10760-10803  _classify_pool_anonymity
 10806-10823  _classify_pool_anonymity_bg
   897-919    _claude_chat_sync_metered
  9916-9922   _client_ip
 21790-21817  _clip_prune
 21820-21830  _clip_recfile_for
 22243-22249  _clip_should_velocity
 21872-21954  _clip_to_discord
  3756-3765   _close_ai_session
 22773-22788  _cohost_broadcast
 22758-22759  _cohost_cfg
 22814-22826  _cohost_fire_highlight
 22762-22770  _cohost_gate
 22791-22811  _cohost_highlight
 10408-10410  _conv_messages
  6897-6958   _cookie_alarm_loop
  2109-2110   _cookie_autofetch_info
  2093-2097   _cookie_autorefresh_info
 24651-24673  _cookie_bezug_loop
 24676-24701  _cookie_bezug_runde
  1996-2000   _cookie_header
  9925-9930   _cookie_sicher
  2122-2136   _cookies_selbst_holen
  4086-4088   _create_index_safe
 20676-20790  _crowdsec_status
 20622-20673  _crowdsec_via_lapi
 20526-20544  _cscli_bin
 20553-20566  _cscli_path
  6787-6812   _daily_summary_loop
 20584-20601  _darf_journal_lesen
  3081-3106   _darf_ytdlp_nachschlagen
 11958-11979  _dashboard_adresse
 21186-21209  _db_maintenance_loop
  6756-6784   _db_vacuum_loop
 16232-16256  _detect_foreign_ad
  1586-1597   _diag_path_owner
 17520-17565  _director_finalize
 18483-18490  _director_for
 17469-17517  _director_mark
 22106-22109  _disc_state_get
 22112-22119  _disc_state_set
 21114-21123  _discord_bot_starten
 21077-21088  _discord_einladung_merken
 21126-21130  _discord_invite
 21091-21111  _discord_kontext
 22067-22103  _discord_live_thread
 17672-17684  _discord_notify
 21049-21074  _discord_ops_alert
 21965-22063  _discord_post_user
 21709-21715  _discord_stop
  6815-6892   _disk_alarm_loop
 24576-24625  _disk_autoclean
 24799-24812  _disk_guard_loop
 13825-13832  _drossel_hoeher
 13821-13822  _drossel_stufe
 13835-13843  _drossel_zuruecksetzen
 12135-12137  _dump_all_threads
 24289-24303  _einstellungen_startzeile
 10686-10749  _enrich_proxies_with_geo
  2165-2226   _ensure_cookie_file_netscape
  8920-8923   _ensure_notify_topic
 10930-10967  _ensure_proxy_ready
  8874-8901   _ensure_topic
   739-741    _env_int
   744-746    _env_int_range
 17717-17730  _event_webhook
 12813-12826  _evolution_loop
  5940-5974   _extract_file_payload
  2298-2300   _extract_urls_from_streamurl_node
 20569-20576  _f2b_sudo_hint
 25404-25467  _fatal_vom_botteil
 24198-24213  _fd_grenze_anheben
  4715-4725   _fehler_text
 10587-10605  _fetch_proxy_list
 18270-18298  _fetch_tiktok_room_id
   822-825    _ff_cmd
 13654-13659  _find_chromium
  3472-3474   _find_external_recorder
  2303-2305   _find_stream_urls
 12513-12538  _fire_webhooks
  7724-7733   _fork_safe
   930-943    _freeai_chat_sync_metered
 20615-20619  _geo_lookup_ips
  3744-3753   _get_ai_session
  7557-7597   _get_live_info
  2932-2939   _get_resolve_semaphore
  8120-8514   _handle_single_tracking
 24398-24400  _hb
 24403-24420  _hb_while
 13101-13103  _highlight_cfg
 13106-13135  _highlight_observe
 13662-13680  _htmlov_screenshot_cmd
 17976-17986  _httpx_proxy
 12546-12558  _in_quiet_hours
 25232-25243  _init_db_oder_abbruch
 26051-26082  _install_fast_eventloop
  9779-9833   _install_fast_json
 12140-12156  _install_faulthandler
 19231-19240  _intel_ensure_schema
 19283-19318  _intel_index_loop
 19252-19267  _intel_index_one
 19243-19249  _intel_semantic
  5240-5249   _is_authorized
  8006-8027   _is_dead
  2288-2290   _is_hevc
 20604-20606  _is_private_ip
  1805-1812   _is_process_running
  6528-6535   _is_quiet_hours
  1379-1388   _is_upload_window
  4580-4595   _iso
  9933-9939   _ist_lokal
  9868-9881   _json_error_handler
  6750-6751   _kick_broadcaster_id
  7913-7920   _kick_cluster_gefunden
  7884-7910   _kick_cluster_weiter
  6662-6704   _kick_follower_count
  6646-6649   _kick_slug
 11590-11597  _kick_user_token
  7856-7881   _kick_ws_pause
 25220-25229  _kickmod_boot
  4170-4173   _kind_from_filename
 12575-12577  _latest_popularity
  1742-1751   _laufstand
 24759-24796  _laufstand_loop
 24322-24360  _leistung_erheben
 18889-18938  _live_react_loop
 18556-18878  _live_react_worker
  3322-3434   _live_status_aufloesen
 17118-17129  _live_transcript_push
 18880-18887  _live_users
 17568-17612  _living_title_loop
 21352-21424  _local_backup_scan
  9850-9864   _log_5xx
 24363-24395  _log_schleuse_pruefen
   812-819    _log_sicher
 14249-14261  _looks_like_codec_err
 14244-14246  _looks_like_source_expired
  7774-7804   _loop_fehler
 12160-12169  _loop_heartbeat
 24104-24137  _loop_lag_monitor
 24151-24171  _loop_stockung_melden
 24174-24184  _loop_takt_starten
 12172-12245  _loop_watchdog_thread
 16995-17012  _loyalty_add
 16986-16992  _loyalty_get
 17015-17023  _loyalty_top
 12685-12687  _manual_donations_total
  4922-4941   _manual_status
  8029-8030   _mark_dead
 11206-11222  _marketing_loop
 22674-22692  _maybe_handle_command
 24898-24922  _maybe_hype_clip
 21759-21787  _meme_klassifizieren
  4073-4078   _migrate_columns
 22953-22964  _mod_is_exempt
 22967-22972  _mod_warn_first
 22975-22978  _mod_warn_text
 12870-12889  _modlog
 12853-12867  _modlog_schreiben
  1075-1077   _multistream_targets
  3109-3145   _nachschlag_ytdlp
  7736-7737   _nc_create_subprocess_exec
  7740-7741   _nc_create_subprocess_shell
 11527-11544  _news_loop
 12912-12914  _normalize_ingest
  2521-2538   _note_check_duration
  8914-8917   _notify_topic_name
  3148-3168   _ohne_url_melden
 17144-17152  _oracle_memories
 17418-17452  _oracle_memorize
 17155-17168  _oracle_persona
 17137-17141  _oracle_recent_text
 13288-13289  _ov_atomic_write
 13279-13281  _ov_bar
 16135-16147  _ov_clip_text
 13284-13285  _ov_oneline
 20281-20310  _overlay_push
 13608-13651  _overlay_render_size
 12981-12985  _overlay_session_reset
 20246-20248  _overlay_src_ok
 16219-16229  _own_invites
 13603-13605  _parse_size
 20798-20878  _parse_ssh_attacks
  7159-7192   _pause_resume_cmd
  2047-2091   _persist_refreshed_cookies
  1950-1982   _pick_checked_pull_proxy
  9970-9983   _pin_auth_value
 10030-10031  _pin_clear_fail
 10010-10013  _pin_locked
 10016-10027  _pin_note_fail
  9986-10007  _pin_ok
 20088-20113  _piper_pick_model
 20173-20224  _piper_say
 12475-12510  _post_json_threaded
 13582-13600  _probe_video_size
  1833-1850   _proc_is_recorder
 10899-10927  _proxy_pool_refresh_loop
  1916-1947   _proxy_report_recording
  8612-8650   _pruefstand_melden
 24233-24244  _pruefung_verworfen
 12125-12127  _prune_stall_dumps
 11276-11446  _public_stats
  2113-2119   _pull_proxy_still
 17688-17714  _push_notify
 10199-10201  _pwa_dir
 10656-10671  _quick_validate_proxy
 12541-12543  _quiet_hours_config
 10164-10197  _rate_guard
 16956-16962  _react_warn
  7644-7683   _reap_proc
  9162-9229   _rec_auto_abschalten
  9109-9159   _rec_frueh_getrennt
  8978-9054   _rec_kategorie_melden
  9057-9106   _rec_totstreak_fortschreiben
  2561-2583   _record_check_outcome
   807-809    _redact_stream_urls
 10826-10896  _refresh_proxy_pool
  2338-2429   _resolve_via_html
  2711-2909   _resolve_via_webcast_api_v2
  2972-3057   _resolve_via_ytdlp
 22283-22412  _resolve_youtube_ingest
  2314-2335   _resolver_stumm
 12964-12975  _restream_active_sources
 13931-14055  _restream_avatar_feeder_start
 14058-14067  _restream_avatar_feeder_stop
 18329-18447  _restream_chat_guardian
 13138-13210  _restream_chat_push
 13265-13274  _restream_chat_push_async
 25127-25170  _restream_durchreicher
 13683-13792  _restream_html_overlay_start
 13795-13808  _restream_html_overlay_stop
 12923-12946  _restream_overlay_files
 18942-18974  _restream_platform_state
 19142-19177  _restream_resume_after_restart
 13241-13262  _restream_status_schreiben
 14115-14187  _restream_tts_enqueue_wav
 13544-13576  _restream_tts_feeder
 13541-13542  _restream_tts_fifo_path
 14070-14097  _restream_tts_start
 14099-14113  _restream_tts_stop
 18980-19139  _restream_verify_loop
 21317-21329  _retention_loop
 21311-21314  _retention_scan
  2668-2670   _room_is_abo
  5978-6095   _run_ai_call
 12268-12281  _run_async_from_flask
 20609-20612  _run_priv
 26039-26047  _run_selfcheck_and_exit
 21332-21343  _s3_client
  8056-8107   _safe_send
  4848-4864   _sample_net_throughput
  2613-2643   _schedule_next_check
 21265-21308  _scheduler_loop
  4081-4083   _schema_pk
 12285-12290  _scraper_session
 22981-23020  _screen_full
 11641-11678  _sec_headers
  2293-2295   _select_stream_from_data_section
 25759-26036  _selfcheck
  8926-8960   _send_live_notice
  1402-1406   _should_defer_upload
 21833-21869  _shrink_for_discord
 10204-10216  _sicheres_ziel
 21145-21183  _sicherheits_erinnerung_loop
 24819-24836  _sign_health_check
 24839-24858  _sign_health_loop
  4598-4623   _sitzung_bestimmen
  7753-7764   _spawn
 26464-26494  _spawn_from_flask
 24247-24253  _speicher_maps
 24256-24271  _speicher_pflegen
 17988-18267  _start_chat_listener
 24216-24230  _start_gesperrt
 12248-12265  _start_loop_watchdog
 11473-11522  _stats_loop
 11452-11455  _stats_output_path
 11458-11470  _stats_write
 20125-20139  _stimme_saubern
 20146-20170  _stimme_schon_gesagt
  8593-8609   _storage_cleanup_loop
 24878-24885  _story_for
  3497-3503   _stream_url_expiry
  3505-3510   _stream_url_ttl
 16182-16189  _streamer_persona_get
 21449-21601  _system_backup
 21610-21640  _system_backup_loop
 12085-12103  _task_auf_bot_schleife
 23794-23810  _telegram_befehlsmenue
  7807-7853   _telegram_polling_fehler
 10608-10647  _test_proxy
 11154-11170  _testpush_resolve_live
  8032-8053   _tg_sprache_setzen
  8833-8843   _tg_topics_load_into_mem
  8830-8831   _tg_topics_path
  8845-8852   _tg_topics_save
  9942-9952   _token_ok
  8855-8859   _topic_forget
 12561-12572  _tracking_max_duration
  4378-4392   _tracking_remove_cleanup
  4409-4421   _tracking_resume_cleanup
  1644-1667   _try_attach_file_handler
 20115-20123  _tts_cleanup
 11130-11134  _tunnel_effective
 24628-24648  _tunnel_lage
 24704-24756  _tunnel_wacht_loop
 19611-19664  _twitch_channel_status
 23023-23168  _twitch_chat_loop
 22125-22138  _twitch_clip_versuchen
 22837-22940  _twitch_eventsub_loop
  1425-1438   _upload_queue_add
  1449-1451   _upload_queue_count
  1408-1417   _upload_queue_load
  1398-1400   _upload_queue_path
  1440-1447   _upload_queue_remove
  1419-1423   _upload_queue_save
  1453-1494   _upload_window_loop
  7617-7624   _uptime_s
 12900-12909  _url_host
  3171-3270   _url_nachschlag
   890-894    _usage_record_claude
 24992-25014  _v37_pause_source
 24956-24966  _v37_restream_restart
 24969-24989  _v37_unpause_source
  7955-7999   _verbindung_verloren
  6707-6738   _viewer_sample_loop
 10034-10037  _wants_html
  7627-7641   _warn_empty_env
 24441-24562  _watchdog_loop
 22558-22566  _wchat_thank_ok
 17756-17786  _whisper_get_model
  7714-7721   _whisper_native_section
 16943-16949  _whisper_pool
 17880-17912  _whisper_segments
 17788-17804  _whisper_stumm
 17807-17877  _whisper_transcribe
 13336-13498  _write_restream_overlay
 13298-13333  _write_restream_overlay_async
 23192-23288  _youtube_api_chat_loop
 19667-19770  _youtube_api_status
 19773-19840  _youtube_channel_status
 23291-23452  _youtube_chat_loop
 22141-22166  _youtube_clip_versuchen
 22418-22431  _youtube_restream_autoconfig
 22434-22458  _youtube_restream_autoconfig_inner
 22525-22553  _youtube_send
 19908-19949  _youtube_set_channel
 22461-22495  _yt_access_token
 22498-22513  _yt_live_chat_id
 22521-22522  _yt_sendrate_cfg
 23171-23186  _yt_timeout
  2956-2957   _ytdlp_detect_available
  2959-2970   _ytdlp_note_result
 12130-12132  _zombie_child_count
 24306-24319  _zustand_kennzahlen
  7493-7517   about
  4289-4293   add_ai_log_entry
  4206-4209   add_archive_entry
  4886-4888   add_archive_rule
  4626-4697   add_recording
  4353-4370   add_tracking
  6098-6131   ai
  3896-3977   ai_chat
  4011-4021   ai_history_append
  4023-4028   ai_history_clear
  4000-4009   ai_history_load
  3985-3998   ai_rate_limit_check
  6160-6168   aireset
 17285-17304  azrael_chat
 23457-23579  brain_cmd
  3513-3518   build_recording_cmd
  4373-4376   bulk_add_trackings
  6961-7020   bulkadd
  8653-8813   check_all_trackings
  4425-4437   claim_live_transition
 16259-16875  class KickModerator
 14264-16022  class RestreamManager
  7923-7952   class _KickClusterSuche
 11013-11055  classify_proxy_anonymity
  6206-6404   cleanup
  5176-5182   cleanup_old_recordings
  4571-4578   clear_recording
 22169-22240  clip_moment
  4838-4841   compute_storage_forecast
  7083-7156   cookies_cmd
  4344-4350   count_trackings_for_chat
  4276-4287   decide_preferred_recorder
  4216-4219   delete_archive_entry
  4890-4892   delete_archive_rule
  5635-5782   diag
 23691-23752  einnahmen_cmd
  4832-4835   find_recordings_by_fingerprint
  4237-4253   finish_recording_attempt
  4397-4399   get_all_active_trackings
  4304-4306   get_all_checks
  4699-4702   get_all_recordings
  4781-4783   get_all_tags_with_counts
  4809-4812   get_annotations_for_recording
  4211-4214   get_archive_entry
  4802-4805   get_bookmarked_recordings
  2153-2158   get_cookie_health
  4769-4775   get_event_log
  4260-4274   get_last_recording_attempt
  3273-3315   get_live_status
  5115-5118   get_manual_recordings
  4817-4820   get_or_compute_inspect_sync
  5217-5220   get_outcome_breakdown
  4788-4791   get_priority_poll_interval
  4255-4258   get_recent_recording_attempts
  4704-4707   get_recording_by_id
  4795-4798   get_recording_note
  3684-3713   get_redis
  4333-4336   get_stats
  5170-5174   get_storage_stats
  4910-4912   get_tiktok_status_distribution
  4439-4448   get_tracking_state
  4394-4395   get_trackings_for_group
  5131-5134   get_trash_recordings
  9289-9758   handle_recording_finished
 23786-23791  hilfe_cmd
  4096-4161   init_db
  4882-4884   list_archive_rules
  5420-5458   live
  8110-8118   live_check_worker
  3768-3807   llm_chat
  3830-3860   llm_chat_sync
  3815-3827   llm_list_models
  4728-4761   log_event
  1767-1800   log_recording_failure
  7306-7355   logs_cmd
 25470-25749  main
  6134-6157   on_ai_media
  7432-7458   on_ai_reply
  7461-7490   on_azrael_mention
  7522-7552   on_callback
 17310-17415  oracle_handle
  7195-7198   pause_tracking
  5230-5235   profile_keyboard
  5373-5417   quelle
  7257-7303   quota
  8516-8590   reaper_loop
  4906-4908   record_tiktok_status
  6173-6203   recstatus
  3715-3723   redis_get_json
  3726-3732   redis_set_json
 23813-23823  report_cmd
 11058-11060  report_proxy_result
  2432-2474   resolve_tiktok_live_stream
  5126-5129   restore_recording
  7201-7204   resume_tracking
  4895-4900   run_archive_rules
 23826-24084  run_bot
 11982-12076  run_flask
  4870-4873   sample_bandwidth_for_active
  4296-4302   save_tiktok_check
  4563-4569   set_recording_file
  4402-4406   set_tracking_paused
  5121-5124   soft_delete_recording
  8966-8976   split_and_send_video
  5283-5325   start
  4221-4235   start_recording_attempt
  6407-6445   stats
  5060-5113   stop_manual_recording
  7207-7254   stoprec
  6631-6639   summary_cmd
  7358-7429   sysres
  5784-5928   teststream
  5327-5368   tiktok
  7023-7080   topusers
  5495-5552   track
  5460-5492   track_exact
  5566-5633   tracklist
  4944-5058   trigger_manual_recording
  4524-4561   try_acquire_recording_lock
  5137-5139   universal_search
 23755-23783  unpause_cmd
  5554-5564   untrack
 23582-23688  update_cmd
  4827-4830   update_recording_fingerprint
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
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
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
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        kategorie, plan
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
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
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
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
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, uebersicht, vergessen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
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
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, ist_telegram_chat, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
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
