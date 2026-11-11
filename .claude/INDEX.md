# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11034  GET              /                                                dashboard
 13091  GET              /api/abo/status                                  api_abo_status
 13045  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11822  GET              /api/automation/status                           api_automation_status
 11844  POST             /api/automation/toggle                           api_automation_toggle
 21651  GET              /api/channel/categories                          api_channel_categories
 21657  POST             /api/channel/set                                 api_channel_set
 21504  GET              /api/channels/status                             api_channels_status
 21178  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21161  GET              /api/clips                                       api_clips
 21207  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21079  GET              /api/debug/threads                               api_debug_threads
 13056  GET              /api/events                                      api_events
 12535  GET              /api/events/stream                               api_events_stream
 12362  GET              /api/health                                      api_health
 21120  POST             /api/highlights/config                           api_highlights_config
 10964  POST             /api/login                                       dashboard_login_submit
 13381  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12450  GET              /api/notify/status                               api_notify_status
 12461  POST             /api/notify/test                                 api_notify_test
 13145  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13122  GET              /api/proxy/trend                                 api_proxy_trend
 21227  GET              /api/tts/<fn>                                    api_tts_file
 22001  GET              /api/upload_window                               api_upload_window
 12652  GET              /archive/<int:eid>/download                      archive_download
 12680  GET              /download/<int:recording_id>                     download
 12609  GET              /health                                          health
 20986  GET              /healthz                                         healthz
 10955  GET              /login                                           dashboard_login_page
 10989  GET              /logout                                          dashboard_logout
 10996  GET              /manifest.webmanifest                            pwa_manifest
 21974  GET              /overlay                                         overlay_page
 11020  GET              /pwa-icon-<variant>.png                          pwa_icon
 11006  GET              /sw.js                                           pwa_service_worker
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
  2273  /about                  Ueber diesen Bot
   977  /ai                     
  2273  /aireset                KI-Kontext zuruecksetzen
  1392  /ask                    
  1078  /assign_role            
  1128  /ban                    
  2228  /botstats               
  2273  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2273  /bulkadd                Mehrere User auf einmal tracken · a b c
  2273  /cleanup                Alte Aufnahmen aufraeumen
  1658  /clearwarns             
  2192  /clip                   
  2177  /clipoftheweek          
  1528  /clips                  
  2273  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1033  /create_category        
  1004  /create_channel         
  1068  /create_group           
  1043  /create_role            
  1019  /create_voice           
  1269  /daily                  
  2273  /diag                   Vollstaendige Diagnose
  2273  /einnahmen              Einnahmen und Spenden
  1421  /event                  
  1463  /events                 
  1568  /follow                 
  1557  /help                   
  1118  /kick                   
  1244  /leaderboard            
  2273  /live                   Live-Status sofort pruefen · @user
  1515  /livenow                
  2273  /logs                   Letzte Fehler aus dem Log
  2273  /pause                  Tracking pausieren · @user
  1543  /post_test              
  1353  /profile                
  1150  /purge                  
  2273  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2273  /quota                  Speicher-Quota
  1231  /rank                   
  1503  /recstatus              
  1088  /remove_role            
  2273  /report                 Azrael-Sentinel-Wochenreport
   990  /restream_status        
  2273  /resume                 Tracking fortsetzen · @user
  1098  /set_channel_perms      
  1193  /setup_community        
  1210  /setup_targets          
  1489  /spenden                
  1600  /stats                  
   949  /status                 
  2273  /stoprec                Laufende Aufnahme sauber beenden · @user
  1696  /streaminfo             
  2273  /summary                Tageszusammenfassung
  2273  /sysres                 System-Ressourcen
  2273  /teststream             Recorder-Selbsttest · @user
  2273  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1138  /timeout                
  1668  /topstreamers           
  2273  /topusers               Top-Streamer nach Aufnahmen
   879  /track                  
  2273  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   962  /tracklist              
  1582  /unfollow               
  2273  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   911  /untrack                
  1621  /warn                   
  1644  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2440  on_member_join
  2397  on_message
  2294  on_raw_reaction_add
  2475  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1773-1824   _award_xp
   536-563    _bereich_umziehen
   483-493    _clip_kopieren
  1995-2024   _clip_week_leader
  2048-2062   _clipoftheweek_loop
  2592-2654   _community_events_loop
  1730-1752   _dc_client
  1755-1764   _dc_offen
  2694-2729   _disc_automod_check
   409-414    _disc_sprache_setzen
  1827-1875   _discord_ai_automod
   685-724    _discord_automod
  1878-1898   _discord_azrael_reply
  2065-2551   _discord_run_once
   244-302    _discord_start
   305-359    _ensure_discord_invite
  2557-2589   _ensure_error_channel
   430-443    _ensure_rank_roles
   842-856    _ensure_team_roles
  2657-2687   _error_channel_loop
   734-738    _guard
   654-682    _handle_voice_ai
   417-427    _is_admin
   508-533    _link_video
  1943-1954   _liveboard_loop
   741-774    _on_level_up
   650-651    _par_chat_id
  2027-2045   _post_clip_of_week
  1957-1975   _post_weekly_digest
   446-472    _provision_base_channels
  1495-1589   _reg_betrieb
  1164-1258   _reg_community_setup
  1261-1342   _reg_daily_profil
  1385-1482   _reg_frage_events
   936-992    _reg_info
  1110-1161   _reg_moderation
  1345-1382   _reg_profil
  1059-1107   _reg_rollen
   995-1056   _reg_server
  1485-1492   _reg_spenden
  1592-1679   _reg_streamer
  1682-1727   _reg_system
   870-933    _reg_tracking
   809-839    _run_tg_handler
   637-647    _tracked_usernames
   161-223    _uebernehmen
   496-505    _umzugsmarken
  1907-1940   _update_liveboard
  1978-1992   _weekly_digest_loop
   475-480    _ziel_guild
   566-608    _ziele_abgleichen
   617-634    _ziele_sync_loop
   611-614    _ziele_takt_min
   226-229    starte
```

## Top-Level-Symbole in bot.py (598 Funktionen, 4 Klassen)

```
 27120-27142  _abbruch_datenbank_unlesbar
  2830-2831   _abo_key
  2851-2869   _abo_probe_dump
 27238-27254  _abschied_wachen
 27257-27275  _abschluss
 17254-17261  _ad_allowlist
 18416-18422  _agent_for
 18425-18441  _ai_telemetry
 18938-18956  _alert
 22869-22919  _alert_monitor_loop
 19632-19689  _alte_beilagen_einsammeln
 23301-23363  _announce_loop
  3730-3740   _anthropic_key
  3747-3749   _anthropic_model
 10598-10601  _arg_int
  2822-2827   _as_dict
 26806-26815  _async_exc_handler
 19126-19148  _audio_tap_cmd
 20152-20211  _audio_tap_melden
 19162-19186  _audio_tap_sammler
  9944-9981   _aufnahme_beim_stopp_sichern
 19574-19595  _aufnahme_chat_ausklang
 19558-19571  _aufnahme_chat_beginnen
 19717-19738  _aufnahme_chat_dienst
 19911-19964  _aufnahme_chat_einarbeiten
 19553-19555  _aufnahme_chat_modus
 19741-19790  _aufnahme_chat_nachtrag
 19598-19629  _aufnahme_chat_vormerken
 19708-19714  _aufnahme_chat_wecken
 26000-26002  _aufnahme_deckel
 19793-19814  _aufnahme_fertigmachen
 23538-23591  _aufnahme_nach_discord
  9984-10002  _aufnahme_platz_frei
  9887-9914   _aufnahme_verteilen
 27202-27222  _aufnahmen_abschliessen
 27145-27199  _aufraeumen
 10797-10866  _auth_cookie
 10755-10793  _auth_guard
  2057-2062   _auto_on
 20838-20856  _auto_restream_loop
 14726-14768  _avatar_frames_laden
 17304-17317  _azrael_brain_kontext
 24497-24512  _azrael_broadcast_reply
 24397-24419  _azrael_chat_reply
 24369-24394  _azrael_chat_should_reply
 24425-24427  _azrael_gate_cfg
 18446-18460  _azrael_live_state
 21887-21901  _azrael_overlay_state
 18820-18874  _azrael_proactive_loop
 18264-18320  _azrael_reaction_to_chats
 24430-24437  _azrael_reply_all_chats
 24356-24366  _azrael_self_names
 24465-24494  _azrael_send_to
 14687-14723  _azrael_spricht
 15034-15047  _azrael_stimme_stumm
 18466-18487  _azrael_system
 23003-23006  _backup_active
 23084-23097  _backup_loop
 26089-26093  _betrieb
 26879-26888  _brain_crowdsec_snap
 27047-27050  _brain_db_health
 22790-22799  _brain_growth_loop
 11213-11240  _brain_growth_snapshot
  2741-2775   _brain_hint_delay
 26951-26986  _brain_moderation_snap
  6736-6764   _brain_notify
 27053-27075  _brain_recording_snap
 26891-26948  _brain_restream_health
 27078-27091  _brain_tiktok_status_snap
 12514-12531  _browser_push
  6776-6863   _build_daily_summary
 15081-15085  _build_restream_cmd
  5488-5515   _can_stop_tracking
  2170-2192   _capture_set_cookies
 13199-13202  _cfg_get
 13205-13207  _cfg_set
 21612-21647  _channel_set_all
 13778-13781  _chat_connected
 13784-13800  _chat_disconnected
 19702-19705  _chat_einarbeiten_async
  9382-9412   _chat_is_forum
 19522-19547  _chat_listener_abbauen
  9554-9589   _chat_migriert
  9592-9593   _chat_migriert_async
 13820-13822  _chat_sanitize
 13763-13775  _chat_stat
 13803-13806  _chat_stats_snapshot
  4053-4065   _check_ai_models_sync
 11495-11538  _classify_pool_anonymity
 11541-11558  _classify_pool_anonymity_bg
   906-928    _claude_chat_sync_metered
 10630-10636  _client_ip
 23996-24010  _clip_chat_ass
 23447-23481  _clip_prune
 23484-23494  _clip_recfile_for
 23916-23984  _clip_schneiden
 24013-24019  _clip_should_velocity
 23594-23679  _clip_to_discord
 19882-19887  _clips_abwarten
  3934-3943   _close_ai_session
 24543-24558  _cohost_broadcast
 24528-24529  _cohost_cfg
 24584-24596  _cohost_fire_highlight
 24532-24540  _cohost_gate
 24561-24581  _cohost_highlight
 11143-11145  _conv_messages
  7160-7221   _cookie_alarm_loop
  2260-2261   _cookie_autofetch_info
  2244-2248   _cookie_autorefresh_info
 26513-26535  _cookie_bezug_loop
 26538-26563  _cookie_bezug_runde
  2147-2151   _cookie_header
 10639-10644  _cookie_sicher
  2273-2287   _cookies_selbst_holen
  4274-4276   _create_index_safe
 22333-22447  _crowdsec_status
 22279-22330  _crowdsec_via_lapi
 22183-22201  _cscli_bin
 22210-22223  _cscli_path
  7044-7071   _daily_summary_loop
 22241-22258  _darf_journal_lesen
  3255-3280   _darf_ytdlp_nachschlagen
 12695-12716  _dashboard_adresse
  1509-1539   _dashboard_trackings_umziehen
 23987-23993  _datei_weg
 22843-22866  _db_maintenance_loop
  6994-7041   _db_vacuum_loop
 17277-17301  _detect_foreign_ad
  1737-1748   _diag_path_owner
 18725-18770  _director_finalize
 20141-20148  _director_for
 18674-18722  _director_mark
 23829-23832  _disc_state_get
 23835-23842  _disc_state_set
 22771-22780  _discord_bot_starten
 22734-22745  _discord_einladung_merken
 22783-22787  _discord_invite
 22748-22768  _discord_kontext
 23790-23826  _discord_live_thread
 18877-18889  _discord_notify
 22706-22731  _discord_ops_alert
 23690-23786  _discord_post_user
 23366-23372  _discord_stop
  7074-7155   _disk_alarm_loop
 26384-26435  _disk_autoclean
 26661-26674  _disk_guard_loop
 14665-14672  _drossel_hoeher
 14661-14662  _drossel_stufe
 14675-14683  _drossel_zuruecksetzen
 12872-12874  _dump_all_threads
 26096-26110  _einstellungen_startzeile
 11421-11484  _enrich_proxies_with_geo
  2316-2377   _ensure_cookie_file_netscape
  9483-9486   _ensure_notify_topic
 11665-11702  _ensure_proxy_ready
  9422-9445   _ensure_topic
   747-749    _env_int
   752-754    _env_int_range
 18922-18935  _event_webhook
 13546-13559  _evolution_loop
  6177-6211   _extract_file_payload
  2449-2451   _extract_urls_from_streamurl_node
 22226-22233  _f2b_sudo_hint
  1495-1506   _fanout_ziele
 27278-27341  _fatal_vom_botteil
 26005-26020  _fd_grenze_anheben
  4948-4958   _fehler_text
 11322-11340  _fetch_proxy_list
 19491-19519  _fetch_tiktok_room_id
   832-835    _ff_cmd
 19895-19908  _ffprobe_masse
 14609-14625  _fifo_schreiber_wecken
 14419-14424  _find_chromium
  3650-3652   _find_external_recorder
  2454-2456   _find_stream_urls
 13250-13275  _fire_webhooks
  8044-8054   _fork_safe
   939-952    _freeai_chat_sync_metered
 22272-22276  _geo_lookup_ips
  3922-3931   _get_ai_session
  7872-7912   _get_live_info
  3106-3113   _get_resolve_semaphore
  8571-8991   _handle_single_tracking
 26205-26207  _hb
 26210-26227  _hb_while
 10870-10887  _herkunft_guard
 13834-13836  _highlight_cfg
 13839-13868  _highlight_observe
 14470-14478  _htmlov_bild_schreiben
 14448-14467  _htmlov_dauerbrowser
 14427-14445  _htmlov_screenshot_cmd
 19188-19198  _httpx_proxy
 13283-13295  _in_quiet_hours
 27106-27117  _init_db_oder_abbruch
 27928-27959  _install_fast_eventloop
 10493-10547  _install_fast_json
 12877-12893  _install_faulthandler
 20889-20898  _intel_ensure_schema
 20941-20976  _intel_index_loop
 20910-20925  _intel_index_one
 20901-20907  _intel_semantic
  5473-5486   _is_authorized
  8397-8418   _is_dead
  2439-2441   _is_hevc
 22261-22263  _is_private_ip
  1956-1963   _is_process_running
  6766-6773   _is_quiet_hours
  1397-1406   _is_upload_window
  4813-4828   _iso
 10647-10653  _ist_lokal
 10582-10595  _json_error_handler
  6988-6989   _kick_broadcaster_id
  8272-8279   _kick_cluster_gefunden
  8207-8269   _kick_cluster_weiter
  6900-6942   _kick_follower_count
  6884-6887   _kick_slug
 12327-12334  _kick_user_token
  8177-8204   _kick_ws_pause
 27094-27103  _kickmod_boot
  4358-4361   _kind_from_filename
 26479-26482  _lagebild_discord_aufnahme
 26492-26496  _lagebild_kick_chat
 26485-26489  _lagebild_overlay
 26499-26501  _lagebild_spendenziel
 26466-26476  _lagebild_upload
 13312-13314  _latest_popularity
  1893-1902   _laufstand
 26621-26658  _laufstand_loop
 26129-26167  _leistung_erheben
  7746-7773   _link_video_senden
  8558-8569   _live_check_frist_melden
 20547-20596  _live_react_loop
 20214-20536  _live_react_worker
  3498-3612   _live_status_aufloesen
 18323-18334  _live_transcript_push
 20538-20545  _live_users
 18773-18817  _living_title_loop
 23009-23081  _local_backup_scan
  4753-4776   _lock_update
 10564-10578  _log_5xx
 26170-26202  _log_schleuse_pruefen
   822-829    _log_sicher
 15093-15105  _looks_like_codec_err
 15088-15090  _looks_like_source_expired
  8095-8125   _loop_fehler
 12897-12906  _loop_heartbeat
 25911-25944  _loop_lag_monitor
 25958-25978  _loop_stockung_melden
 25981-25991  _loop_takt_starten
 12909-12982  _loop_watchdog_thread
 18200-18217  _loyalty_add
 18191-18197  _loyalty_get
 18220-18228  _loyalty_top
  5155-5174   _manual_status
  8420-8421   _mark_dead
 11941-11957  _marketing_loop
 24444-24462  _maybe_handle_command
 26760-26784  _maybe_hype_clip
 23416-23444  _meme_klassifizieren
 19817-19879  _meme_zusammenschnitt
  4261-4266   _migrate_columns
 24726-24737  _mod_is_exempt
 24740-24745  _mod_warn_first
 24748-24751  _mod_warn_text
 13603-13622  _modlog
 13586-13600  _modlog_schreiben
  1093-1095   _multistream_targets
  3283-3319   _nachschlag_ytdlp
  8057-8058   _nc_create_subprocess_exec
  8061-8062   _nc_create_subprocess_shell
 12264-12281  _news_loop
 13645-13647  _normalize_ingest
  2672-2689   _note_check_duration
  9477-9480   _notify_topic_name
  2876-2882   _offline_ergebnis
  3322-3345   _ohne_url_melden
 18349-18357  _oracle_memories
 18623-18657  _oracle_memorize
 18360-18373  _oracle_persona
 18342-18346  _oracle_recent_text
 14043-14044  _ov_atomic_write
 14034-14036  _ov_bar
 17180-17192  _ov_clip_text
 14039-14040  _ov_oneline
 21938-21967  _overlay_push
 14373-14416  _overlay_render_size
 13714-13718  _overlay_session_reset
 21903-21905  _overlay_src_ok
 14053-14065  _overlay_takt
 17264-17274  _own_invites
 14368-14370  _parse_size
 22455-22535  _parse_ssh_attacks
  7422-7455   _pause_resume_cmd
  2198-2242   _persist_refreshed_cookies
  2101-2133   _pick_checked_pull_proxy
 10684-10697  _pin_auth_value
 10744-10745  _pin_clear_fail
 10724-10727  _pin_locked
 10730-10741  _pin_note_fail
 10700-10721  _pin_ok
 21745-21770  _piper_pick_model
 21830-21881  _piper_say
 13212-13247  _post_json_threaded
 14347-14365  _probe_video_size
  1984-2001   _proc_is_recorder
 11634-11662  _proxy_pool_refresh_loop
  2067-2098   _proxy_report_recording
  9130-9211   _pruef_runde
  9089-9127   _pruefstand_melden
 26040-26051  _pruefung_verworfen
 12862-12864  _prune_stall_dumps
 12011-12183  _public_stats
  2264-2270   _pull_proxy_still
 18893-18919  _push_notify
 10934-10936  _pwa_dir
 11391-11406  _quick_validate_proxy
 13278-13280  _quiet_hours_config
 10899-10932  _rate_guard
 18161-18167  _react_warn
  7959-7998   _reap_proc
  9817-9884   _rec_auto_abschalten
  9764-9814   _rec_frueh_getrennt
  9633-9709   _rec_kategorie_melden
  9712-9761   _rec_totstreak_fortschreiben
  2712-2734   _record_check_outcome
   817-819    _redact_stream_urls
 11561-11631  _refresh_proxy_pool
  2489-2580   _resolve_via_html
  2885-3083   _resolve_via_webcast_api_v2
  3146-3231   _resolve_via_ytdlp
 24053-24182  _resolve_youtube_ingest
  2465-2486   _resolver_stumm
 13697-13708  _restream_active_sources
 14771-14898  _restream_avatar_feeder_start
 14901-14911  _restream_avatar_feeder_stop
 19967-20105  _restream_chat_guardian
 13871-13943  _restream_chat_push
 14020-14029  _restream_chat_push_async
 26989-27044  _restream_durchreicher
 14481-14606  _restream_html_overlay_start
 14628-14648  _restream_html_overlay_stop
 13656-13679  _restream_overlay_files
 20600-20632  _restream_platform_state
 20800-20835  _restream_resume_after_restart
 13974-13991  _restream_soll_schreiben
 13994-14017  _restream_status_schreiben
 14959-15031  _restream_tts_enqueue_wav
 14309-14341  _restream_tts_feeder
 14306-14307  _restream_tts_fifo_path
 14914-14941  _restream_tts_start
 14943-14957  _restream_tts_stop
 20638-20797  _restream_verify_loop
 22974-22986  _retention_loop
 22968-22971  _retention_scan
  2833-2835   _room_is_abo
  6215-6332   _run_ai_call
 13005-13018  _run_async_from_flask
 22266-22269  _run_priv
 27916-27924  _run_selfcheck_and_exit
 22989-23000  _s3_client
  8447-8517   _safe_send
  5081-5097   _sample_net_throughput
  2778-2808   _schedule_next_check
 22922-22965  _scheduler_loop
  4269-4271   _schema_pk
 13022-13027  _scraper_session
 24754-24793  _screen_full
 12378-12415  _sec_headers
  2444-2446   _select_stream_from_data_section
 27633-27913  _selfcheck
  9489-9523   _send_live_notice
  1420-1424   _should_defer_upload
 23497-23535  _shrink_for_discord
 10939-10951  _sicheres_ziel
 22802-22840  _sicherheits_erinnerung_loop
 26681-26698  _sign_health_check
 26701-26720  _sign_health_loop
  4831-4856   _sitzung_bestimmen
  8074-8085   _spawn
 28347-28377  _spawn_from_flask
 26054-26060  _speicher_maps
 26063-26078  _speicher_pflegen
 19200-19488  _start_chat_listener
 26023-26037  _start_gesperrt
 12985-13002  _start_loop_watchdog
 12210-12259  _stats_loop
 12189-12192  _stats_output_path
 12195-12207  _stats_write
 21782-21796  _stimme_saubern
 21803-21827  _stimme_schon_gesagt
  9070-9086   _storage_cleanup_loop
 26740-26747  _story_for
  3675-3681   _stream_url_expiry
  3683-3688   _stream_url_ttl
 17227-17234  _streamer_persona_get
 23106-23258  _system_backup
 23267-23297  _system_backup_loop
 12822-12840  _task_auf_bot_schleife
 25591-25607  _telegram_befehlsmenue
  8128-8174   _telegram_polling_fehler
  1465-1492   _telegram_ziele
 11343-11382  _test_proxy
 11889-11905  _testpush_resolve_live
 19890-19892  _text_schreiben
  9541-9551   _tg_migriert_laden
  9537-9538   _tg_migriert_pfad
  8423-8444   _tg_sprache_setzen
  9351-9361   _tg_topics_load_into_mem
  9348-9349   _tg_topics_path
  9363-9370   _tg_topics_save
 10656-10666  _token_ok
  9448-9464   _topic_anlegen
  9373-9380   _topic_forget
 13298-13309  _tracking_max_duration
  4566-4580   _tracking_remove_cleanup
  4597-4609   _tracking_resume_cleanup
  1795-1818   _try_attach_file_handler
 21772-21780  _tts_cleanup
 11865-11869  _tunnel_effective
 26438-26458  _tunnel_lage
 26566-26618  _tunnel_wacht_loop
 21271-21324  _twitch_channel_status
 24796-24944  _twitch_chat_loop
 23848-23861  _twitch_clip_versuchen
 24607-24713  _twitch_eventsub_loop
  1585-1620   _upload_queue_abarbeiten
  1443-1463   _upload_queue_add
  1556-1558   _upload_queue_count
  1426-1435   _upload_queue_load
  1623-1645   _upload_queue_nachher
  1416-1418   _upload_queue_path
  1542-1546   _upload_queue_remove
  1437-1441   _upload_queue_save
  1549-1554   _upload_queue_update
  9917-9941   _upload_rest_sichern
  1560-1582   _upload_window_loop
  7932-7939   _uptime_s
 13633-13642  _url_host
  3348-3446   _url_nachschlag
   899-903    _usage_record_claude
 26854-26876  _v37_pause_source
 26818-26828  _v37_restream_restart
 26831-26851  _v37_unpause_source
  8346-8390   _verbindung_verloren
  6945-6976   _viewer_sample_loop
 10748-10751  _wants_html
  7942-7956   _warn_empty_env
 26248-26370  _watchdog_loop
 24328-24336  _wchat_thank_ok
 18961-18998  _whisper_get_model
  8033-8041   _whisper_native_section
 18148-18154  _whisper_pool
 19092-19124  _whisper_segments
 19000-19016  _whisper_stumm
 19019-19089  _whisper_transcribe
 14106-14263  _write_restream_overlay
 14068-14103  _write_restream_overlay_async
 24968-25067  _youtube_api_chat_loop
 21327-21430  _youtube_api_status
 21433-21500  _youtube_channel_status
 25070-25234  _youtube_chat_loop
 23864-23889  _youtube_clip_versuchen
 24188-24201  _youtube_restream_autoconfig
 24204-24228  _youtube_restream_autoconfig_inner
 24295-24323  _youtube_send
 21568-21609  _youtube_set_channel
 24231-24265  _yt_access_token
 24268-24283  _yt_live_chat_id
 24291-24292  _yt_sendrate_cfg
 24947-24962  _yt_timeout
  3130-3131   _ytdlp_detect_available
  3133-3144   _ytdlp_note_result
 12867-12869  _zombie_child_count
 26113-26126  _zustand_kennzahlen
  7808-7832   about
  4477-4481   add_ai_log_entry
  4394-4397   add_archive_entry
  5119-5121   add_archive_rule
  4859-4930   add_recording
  4541-4558   add_tracking
  6335-6368   ai
  4079-4165   ai_chat
  4199-4209   ai_history_append
  4211-4216   ai_history_clear
  4188-4197   ai_history_load
  4173-4186   ai_rate_limit_check
  6397-6405   aireset
 18490-18509  azrael_chat
 25239-25361  brain_cmd
  3691-3696   build_recording_cmd
  4561-4564   bulk_add_trackings
  7224-7283   bulkadd
  9214-9330   check_all_trackings
  4613-4625   claim_live_transition
 17320-18080  class KickModerator
 15108-17067  class RestreamManager
  4779-4780   class _AufnahmeLockVerloren
  8282-8343   class _KickClusterSuche
 11748-11790  classify_proxy_anonymity
  6443-6642   cleanup
  5409-5415   cleanup_old_recordings
  4804-4811   clear_recording
 23892-23913  clip_moment
  5071-5074   compute_storage_forecast
  7346-7419   cookies_cmd
  4532-4538   count_trackings_for_chat
  4464-4475   decide_preferred_recorder
  4404-4407   delete_archive_entry
  5123-5125   delete_archive_rule
  5872-6019   diag
 25473-25534  einnahmen_cmd
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
 10005-10472  handle_recording_finished
 25583-25588  hilfe_cmd
  4284-4349   init_db
  5115-5117   list_archive_rules
  5657-5695   live
  8520-8550   live_check_worker
  3946-3989   llm_chat
  4012-4043   llm_chat_sync
  3997-4009   llm_list_models
  4961-4994   log_event
  1918-1951   log_recording_failure
  7569-7618   logs_cmd
 27344-27623  main
  6371-6394   on_ai_media
  7695-7721   on_ai_reply
  7776-7805   on_azrael_mention
  7837-7867   on_callback
  9596-9614   on_chat_migration
  7730-7743   on_link_video
 18515-18620  oracle_handle
  7458-7461   pause_tracking
  5463-5468   profile_keyboard
  5610-5654   quelle
  7520-7566   quota
  8993-9067   reaper_loop
  5139-5141   record_tiktok_status
  6410-6440   recstatus
  3893-3901   redis_get_json
  3904-3910   redis_set_json
 25610-25620  report_cmd
 11793-11795  report_proxy_result
  2583-2625   resolve_tiktok_live_stream
  5359-5362   restore_recording
  7464-7467   resume_tracking
  5128-5133   run_archive_rules
 25623-25891  run_bot
 12719-12813  run_flask
  5103-5106   sample_bandwidth_for_active
  4484-4490   save_tiktok_check
  4783-4802   set_recording_file
  4590-4594   set_tracking_paused
  5354-5357   soft_delete_recording
 25568-25580  spenden_cmd
  9620-9631   split_and_send_video
  5520-5562   start
  4409-4423   start_recording_attempt
  6645-6683   stats
  5293-5346   stop_manual_recording
  7470-7517   stoprec
  6869-6877   summary_cmd
  7621-7692   sysres
  6021-6165   teststream
  5564-5605   tiktok
  7286-7343   topusers
  5732-5789   track
  5697-5729   track_exact
  5803-5870   tracklist
  5177-5291   trigger_manual_recording
  4715-4750   try_acquire_recording_lock
  5370-5372   universal_search
 25537-25565  unpause_cmd
  5791-5801   untrack
 25364-25470  update_cmd
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
clientip.py            echte_ip, ist_https, ist_lokal
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
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
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
