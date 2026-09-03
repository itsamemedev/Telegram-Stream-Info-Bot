# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (116)

```
 10477  GET              /                                                dashboard
 13868  GET              /api/abo/status                                  api_abo_status
 10550  GET              /api/active-recordings                           api_active_recordings
 13939  GET              /api/activity-pulse                              api_activity_pulse
 13746  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20358  GET/POST         /api/audio/config                                api_audio_config
 20388  POST             /api/audio/testtone                              api_audio_testtone
 13812  GET/POST         /api/auto-archive-rules                          api_archive_rules
 13836  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 13840  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11986  GET              /api/automation/status                           api_automation_status
 12008  POST             /api/automation/toggle                           api_automation_toggle
 10849  GET              /api/backoff-watch                               api_backoff_watch
 13308  POST             /api/backup/run                                  api_backup_run
 13274  GET              /api/backup/status                               api_backup_status
 13263  POST             /api/backup/system                               api_backup_system
 13778  GET              /api/bandwidth/live                              api_bandwidth_live
 13731  GET              /api/bookmarks                                   api_bookmarks_list
 11112  GET              /api/brain                                       api_brain
 11049  GET              /api/brain/alarms                                api_brain_alarms
 11034  GET              /api/brain/creator                               api_brain_creator
 11011  GET              /api/brain/graph                                 api_brain_graph
 11072  GET              /api/brain/growth                                api_brain_growth
 10027  GET              /api/brain/health                                api_brain_health
 20916  GET              /api/channel/categories                          api_channel_categories
 20922  POST             /api/channel/set                                 api_channel_set
 20769  GET              /api/channels/status                             api_channels_status
 10531  GET              /api/checks                                      api_checks
 20443  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20426  GET              /api/clips                                       api_clips
 20472  POST/DELETE      /api/clips/clear                                 api_clips_clear
 14247  GET              /api/community/stats                             api_community_stats
 21526  GET              /api/data/export                                 api_data_export
 20251  GET              /api/debug/threads                               api_debug_threads
 22373  GET              /api/defense/attacks                             api_defense_attacks
 22340  GET              /api/defense/crowdsec                            api_defense_crowdsec
 22358  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22064  GET              /api/defense/overview                            api_defense_overview
 13760  GET              /api/events                                      api_events
 13145  GET              /api/events/stream                               api_events_stream
 13773  GET              /api/forecast/storage                            api_forecast_storage
 12024  GET              /api/freeai/status                               api_freeai_status
 12734  GET              /api/health                                      api_health
 13791  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 13787  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20329  GET              /api/highlights                                  api_highlights
 20341  POST             /api/highlights/config                           api_highlights_config
 10411  POST             /api/login                                       dashboard_login_submit
 14232  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14201  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13043  GET              /api/notify/status                               api_notify_status
 13054  POST             /api/notify/test                                 api_notify_test
 10635  GET              /api/outcomes                                    api_outcomes
 21363  POST             /api/overlay/config                              api_overlay_config
 21350  POST             /api/overlay/event                               api_overlay_event
 21255  GET              /api/overlay/state                               api_overlay_state
 10668  GET              /api/profile/<username>                          api_profile
 13957  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 13799  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 13922  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13899  GET              /api/proxy/trend                                 api_proxy_trend
 12479  GET              /api/public/stats                                api_public_stats
 10511  GET              /api/pulse                                       api_pulse
 13367  GET              /api/recording-attempts                          api_recording_attempts
 20053  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20031  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20072  POST             /api/restream/<int:rid>/start                    api_restream_start
 20272  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 21217  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20007  POST             /api/restream/create                             api_restream_create
 12604  GET              /api/restream/deck                               api_restream_deck
 11960  GET              /api/restream/health                             api_restream_health
 21239  POST             /api/restream/layout                             api_restream_layout
 19980  GET              /api/restream/list                               api_restream_list
 11929  POST             /api/restream/report                             api_restream_report
 20285  POST             /api/restream/start_all                          api_restream_start_all
 20311  POST             /api/restream/stop_all                           api_restream_stop_all
 12135  GET              /api/restream/testpush                           api_testpush_status
 12160  POST             /api/restream/testpush                           api_testpush_run
 14332  GET              /api/restream/verify                             api_restream_verify
 13092  GET              /api/retention/preview                           api_retention_preview
 13101  POST             /api/retention/run                               api_retention_run
 13716  GET              /api/search                                      api_search
 22111  GET              /api/selftest                                    api_selftest
 20089  GET              /api/shield/stats                                api_shield_stats
 10572  GET              /api/storage                                     api_storage
 10579  POST             /api/storage/cleanup                             api_storage_cleanup
 13853  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11899  GET              /api/stream/timeline                             api_stream_timeline
 12795  GET              /api/stream/transcript                           api_stream_transcript
 10603  GET              /api/summary/preview                             api_summary_preview
 13432  GET              /api/system                                      api_system
 14280  GET              /api/system/check_timing                         api_check_timing
 14395  GET              /api/system/config_drift                         api_config_drift
 12809  GET              /api/system/config_snapshot                      api_system_config_snapshot
 12901  GET              /api/system/preflight                            api_system_preflight
 13027  GET              /api/system/preflight_history                    api_system_preflight_history
 13210  GET              /api/system/resilience                           api_system_resilience
 13751  GET              /api/tags                                        api_tags_list
 10545  GET              /api/top                                         api_top
 10904  GET              /api/trend-7d                                    api_trend_7d
 20492  GET              /api/tts/<fn>                                    api_tts_file
 21391  GET              /api/upload_window                               api_upload_window
 10649  GET              /api/userstats                                   api_userstats
 12527  GET              /api/version                                     api_version
 13405  GET              /archive/<int:eid>/download                      archive_download
 13462  GET              /download/<int:recording_id>                     download
 13345  GET              /health                                          health
 20220  GET              /healthz                                         healthz
 10402  GET              /login                                           dashboard_login_page
 10432  GET              /logout                                          dashboard_logout
 10439  GET              /manifest.webmanifest                            pwa_manifest
 12837  GET              /metrics                                         api_prometheus_metrics
 21200  GET              /overlay                                         overlay_page
 10463  GET              /pwa-icon-<variant>.png                          pwa_icon
 10449  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (243)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
   154  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    90  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   213  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   111  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   333  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   319  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   341  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   165  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   397  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   388  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   305  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   181  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   222  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   234  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   363  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   272  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   258  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   370  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
    65  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    37  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   227  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   153  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   171  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   143  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    46  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   119  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    57  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    46  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   204  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    70  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   203  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   225  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    84  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   130  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    69  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   109  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   159  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   110  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   158  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   175  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   206  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   182  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   242  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   212  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    73  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   226  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   106  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    58  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    82  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    36  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   114  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   135  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   147  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    72  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
    96  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    50  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   182  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
```

## Discord-Slash-Commands (45)

```
 22837  /ai                     
 23296  /ask                    
 22928  /assign_role            
 22974  /ban                    
 23628  /botstats               
 23552  /clearwarns             
 23592  /clip                   
 23577  /clipoftheweek          
 23419  /clips                  
 22889  /create_category        
 22858  /create_channel         
 22917  /create_group           
 22900  /create_role            
 22874  /create_voice           
 23210  /daily                  
 23326  /event                  
 23369  /events                 
 23465  /follow                 
 23449  /help                   
 22963  /kick                   
 23192  /leaderboard            
 23405  /livenow                
 23435  /post_test              
 23266  /profile                
 22998  /purge                  
 23178  /rank                   
 23392  /recstatus              
 22939  /remove_role            
 22851  /restream_status        
 22950  /set_channel_perms      
 23143  /setup_community        
 23161  /setup_targets          
 23491  /stats                  
 22763  /status                 
 23787  /streaminfo             
 23684  /sys_report             
 23660  /sys_unpause            
 22985  /timeout                
 23563  /topstreamers           
 22793  /track                  
 22777  /tracklist              
 23480  /unfollow               
 22826  /untrack                
 23513  /warn                   
 23537  /warnings               
```

## Discord-Events (4)

```
 24273  on_member_join
 24235  on_message
 23874  on_raw_reaction_add
 24308  on_ready
```

## Top-Level-Symbole in bot.py (496 Funktionen, 2 Klassen)

```
  2506-2507   _abo_key
  2527-2545   _abo_probe_dump
 21633-21643  _active_recorder_sync
 17252-17259  _ad_allowlist
 18390-18396  _agent_for
 21645-21663  _ai_calls_total_sync
 18399-18415  _ai_telemetry
 18903-18921  _alert
 24424-24474  _alert_monitor_loop
 24855-24917  _announce_loop
  3448-3451   _anthropic_key
  3458-3460   _anthropic_model
 10155-10158  _arg_int
  2498-2503   _as_dict
 15079-15084  _audio_cfg
 19057-19079  _audio_tap_cmd
 10323-10334  _auth_cookie
 10290-10319  _auth_guard
  1654-1659   _auto_on
 19956-19974  _auto_restream_loop
 25973-25988  _azrael_broadcast_reply
 25873-25895  _azrael_chat_reply
 25856-25870  _azrael_chat_should_reply
 25901-25903  _azrael_gate_cfg
 18420-18434  _azrael_live_state
 21103-21117  _azrael_overlay_state
 18786-18840  _azrael_proactive_loop
 18238-18294  _azrael_reaction_to_chats
 25906-25913  _azrael_reply_all_chats
 25843-25853  _azrael_self_names
 25941-25970  _azrael_send_to
 18440-18461  _azrael_system
 24593-24596  _backup_active
 24674-24687  _backup_loop
 24386-24395  _brain_growth_loop
 10980-11007  _brain_growth_snapshot
  2434-2454   _brain_hint_delay
 10972-10974  _brain_history_for
  6539-6567   _brain_notify
 10949-10970  _brain_record
 10976-10978  _brain_stream_recent
 13124-13141  _browser_push
  6583-6670   _build_daily_summary
  2937-3117   _build_native_cmd
 15440-15627  _build_restream_cmd
  3161-3194   _build_ytdlp_cmd
 21585-21592  _cached_probe
  5361-5388   _can_stop_tracking
  1834-1856   _capture_set_cookies
 14016-14019  _cfg_get
 14022-14024  _cfg_set
 20877-20912  _channel_set_all
 14677-14680  _chat_connected
 14683-14699  _chat_disconnected
  8635-8646   _chat_is_forum
 14719-14721  _chat_sanitize
 14723-14732  _chat_src_ok
 14662-14674  _chat_stat
 14702-14705  _chat_stats_snapshot
  3723-3734   _check_ai_alive_sync
  3737-3749   _check_ai_models_sync
 21594-21607  _check_redis_alive_sync
 21609-21629  _check_redis_version_sync
 11579-11622  _classify_pool_anonymity
 11625-11642  _classify_pool_anonymity_bg
   812-816    _claude_chat_sync_metered
 10184-10191  _client_ip
 24949-24976  _clip_prune
 24979-24989  _clip_recfile_for
 25502-25508  _clip_should_velocity
 25030-25112  _clip_to_discord
  3621-3630   _close_ai_session
 26019-26034  _cohost_broadcast
 26004-26005  _cohost_cfg
 26060-26072  _cohost_fire_highlight
 26008-26016  _cohost_gate
 26037-26057  _cohost_highlight
 25161-25195  _community_events_loop
 10803-10805  _conv_messages
  6947-6990   _cookie_alarm_loop
  1906-1910   _cookie_autorefresh_info
  1811-1815   _cookie_header
 13174-13206  _cpu_load_snapshot
  3943-3955   _create_index_safe
 21866-21972  _crowdsec_status
 21812-21863  _crowdsec_via_lapi
 21677-21695  _cscli_bin
 21701-21714  _cscli_path
  6837-6862   _daily_summary_loop
 21732-21749  _darf_journal_lesen
 24398-24421  _db_maintenance_loop
  6806-6834   _db_vacuum_loop
 17275-17299  _detect_foreign_ad
  1392-1403   _diag_path_owner
 18692-18736  _director_finalize
 19503-19510  _director_for
 18641-18689  _director_mark
 25396-25431  _disc_automod_check
 25372-25375  _disc_state_get
 25378-25385  _disc_state_set
 22415-22428  _discord_guild_filesize_bytes
 22620-22624  _discord_invite
 25333-25369  _discord_live_thread
 18843-18855  _discord_notify
 22519-22544  _discord_ops_alert
 25231-25329  _discord_post_user
 22680-24383  _discord_run_once
 22559-22617  _discord_start
 24920-24926  _discord_stop
 22436-22438  _discord_upload_limit_label
 22431-22433  _discord_upload_limit_mb
  6865-6942   _disk_alarm_loop
 27456-27505  _disk_autoclean
 27508-27521  _disk_guard_loop
 27448-27453  _disk_pct
 15036-15038  _drawtext_chain
 13559-13561  _dump_all_threads
 11504-11568  _enrich_proxies_with_geo
  2051-2095   _ensure_cookie_file_netscape
 22627-22677  _ensure_discord_invite
 25126-25158  _ensure_error_channel
  8694-8697   _ensure_notify_topic
 11749-11786  _ensure_proxy_ready
  8648-8675   _ensure_topic
   669-671    _env_int
   674-676    _env_int_range
 25198-25228  _error_channel_loop
 18887-18900  _event_webhook
 14482-14495  _evolution_loop
  5981-6015   _extract_file_payload
  2183-2185   _extract_urls_from_streamurl_node
 21717-21724  _f2b_sudo_hint
 18923-18925  _faster_whisper_available
 11393-11411  _fetch_proxy_list
 19337-19365  _fetch_tiktok_room_id
   745-748    _ff_cmd
 15199-15204  _find_chromium
  3154-3158   _find_external_recorder
  2188-2190   _find_stream_urls
 14067-14092  _fire_webhooks
  7726-7735   _fork_safe
   827-836    _freeai_chat_sync_metered
 21767-21809  _geo_lookup_ips
  3610-3619   _get_ai_session
  7560-7600   _get_live_info
  2724-2731   _get_resolve_semaphore
  7990-8356   _handle_single_tracking
 27274-27276  _hb
 27279-27296  _hb_while
 14737-14739  _highlight_cfg
 14742-14771  _highlight_observe
 15207-15225  _htmlov_screenshot_cmd
 19081-19091  _httpx_proxy
 14100-14112  _in_quiet_hours
 28347-28378  _install_fast_eventloop
 10050-10104  _install_fast_json
 13564-13580  _install_faulthandler
 20128-20137  _intel_ensure_schema
 20175-20210  _intel_index_loop
 20149-20159  _intel_index_one
 20140-20146  _intel_semantic
  5350-5359   _is_authorized
  7891-7897   _is_dead
  2173-2175   _is_hevc
 21752-21758  _is_private_ip
  1556-1563   _is_process_running
  6569-6580   _is_quiet_hours
  1193-1202   _is_upload_window
 10139-10152  _json_error_handler
  6792-6793   _kick_broadcaster_id
 12061-12080  _kick_channel_live
  6704-6746   _kick_follower_count
  6688-6691   _kick_slug
 12554-12585  _kick_user_token
  3992-3995   _kind_from_filename
 14129-14134  _latest_popularity
 19718-19751  _live_react_loop
 19514-19707  _live_react_worker
 18297-18308  _live_transcript_push
 19709-19716  _live_users
 18739-18783  _living_title_loop
  1732-1805   _load_cookies_dict
 24599-24671  _local_backup_scan
 10121-10135  _log_5xx
 15635-15647  _looks_like_codec_err
 15630-15632  _looks_like_source_expired
  7807-7837   _loop_fehler
 13584-13593  _loop_heartbeat
 27244-27271  _loop_lag_monitor
 13596-13664  _loop_watchdog_thread
 18177-18191  _loyalty_add
 18168-18174  _loyalty_get
 18194-18202  _loyalty_top
 14266-14268  _manual_donations_total
  7899-7900   _mark_dead
 12232-12248  _marketing_loop
 25920-25938  _maybe_handle_command
 27607-27631  _maybe_hype_clip
  3910-3933   _migrate_columns
 26199-26210  _mod_is_exempt
 26213-26218  _mod_warn_first
 26221-26224  _mod_warn_text
 14522-14530  _modlog
   946-948    _multistream_targets
  7738-7739   _nc_create_subprocess_exec
  7742-7743   _nc_create_subprocess_shell
 12484-12501  _news_loop
 14560-14562  _normalize_ingest
  2365-2382   _note_check_duration
  8688-8691   _notify_topic_name
 18323-18331  _oracle_memories
 18596-18630  _oracle_memorize
 18334-18347  _oracle_persona
 18316-18320  _oracle_recent_text
 14862-14870  _ov_atomic_write
 14850-14856  _ov_bar
 17178-17190  _ov_clip_text
 14859-14860  _ov_oneline
 21167-21196  _overlay_push
 15153-15196  _overlay_render_size
 14624-14628  _overlay_session_reset
 21119-21122  _overlay_src_ok
 17262-17272  _own_invites
 15148-15150  _parse_size
 21980-22060  _parse_ssh_attacks
  7162-7195   _pause_resume_cmd
  1860-1904   _persist_refreshed_cookies
  1698-1730   _pick_checked_pull_proxy
 10220-10233  _pin_auth_value
 10279-10280  _pin_clear_fail
 10259-10262  _pin_locked
 10265-10276  _pin_note_fail
 10236-10256  _pin_ok
 21013-21038  _piper_pick_model
 21050-21097  _piper_say
 14029-14064  _post_json_threaded
 15127-15145  _probe_video_size
  1584-1601   _proc_is_recorder
 11491-11502  _proxy_geo_cache_put
 11718-11746  _proxy_pool_refresh_loop
  1664-1695   _proxy_report_recording
 13549-13551  _prune_stall_dumps
 12302-12423  _public_stats
 18858-18884  _push_notify
 10381-10383  _pwa_dir
 11462-11477  _quick_validate_proxy
 14095-14097  _quiet_hours_config
 10346-10379  _rate_guard
 18142-18148  _react_warn
  7646-7685   _reap_proc
  2405-2427   _record_check_outcome
   740-742    _redact_stream_urls
 11645-11715  _refresh_proxy_pool
  2199-2289   _resolve_via_html
  2547-2701   _resolve_via_webcast_api_v2
  2764-2826   _resolve_via_ytdlp
 25547-25676  _resolve_youtube_ingest
 19790-19797  _restream_active_platforms
 14609-14620  _restream_active_sources
 19368-19467  _restream_chat_guardian
 14774-14846  _restream_chat_push
 14533-14545  _restream_enabled
 15228-15315  _restream_html_overlay_start
 15318-15331  _restream_html_overlay_stop
  1141-1143   _restream_layout_mode
 14571-14594  _restream_overlay_files
 19755-19787  _restream_platform_state
 19918-19953  _restream_resume_after_restart
 15379-15437  _restream_tts_enqueue_wav
 15089-15121  _restream_tts_feeder
 15086-15087  _restream_tts_fifo_path
 15334-15361  _restream_tts_start
 15363-15377  _restream_tts_stop
 19800-19915  _restream_verify_loop
 24564-24576  _retention_loop
 24523-24561  _retention_scan
  2509-2511   _room_is_abo
  6019-6136   _run_ai_call
 13687-13700  _run_async_from_flask
 21761-21764  _run_priv
 28335-28343  _run_selfcheck_and_exit
 24579-24590  _s3_client
  7926-7977   _safe_send
  4614-4630   _sample_net_throughput
  2457-2484   _schedule_next_check
 24477-24520  _scheduler_loop
  3936-3940   _schema_pk
 13704-13709  _scraper_session
 26227-26266  _screen_full
 12750-12787  _sec_headers
  2178-2180   _select_stream_from_data_section
 28148-28332  _selfcheck
  8700-8734   _send_live_notice
  1216-1220   _should_defer_upload
 24992-25027  _shrink_for_discord
 10386-10398  _sicheres_ziel
 27528-27545  _sign_health_check
 27548-27567  _sign_health_loop
  7755-7766   _spawn
  7769-7799   _spawn_from_flask
 22104-22107  _st_befund
 19093-19334  _start_chat_listener
 13667-13684  _start_loop_watchdog
 12447-12475  _stats_loop
 12426-12429  _stats_output_path
 12432-12444  _stats_write
  8428-8444   _storage_cleanup_loop
 27587-27594  _story_for
  3216-3222   _stream_url_expiry
  3231-3237   _stream_url_is_fresh
  3224-3229   _stream_url_ttl
 17225-17232  _streamer_persona_get
 15041-15045  _studio_chain
 24696-24818  _system_backup
 24821-24851  _system_backup_loop
 11414-11453  _test_proxy
 12102-12111  _testpush_cfg
 12114-12131  _testpush_exec
 12083-12099  _testpush_resolve_live
  7902-7923   _tg_sprache_setzen
  8607-8617   _tg_topics_load_into_mem
  8604-8605   _tg_topics_path
  8619-8626   _tg_topics_save
 10194-10202  _token_ok
  8629-8633   _topic_forget
 14115-14126  _tracking_max_duration
  4201-4215   _tracking_remove_cleanup
  4232-4244   _tracking_resume_cleanup
  1450-1473   _try_attach_file_handler
 21040-21048  _tts_cleanup
 12039-12043  _tunnel_effective
 20536-20589  _twitch_channel_status
 26269-26414  _twitch_chat_loop
 26083-26186  _twitch_eventsub_loop
  1239-1252   _upload_queue_add
  1263-1265   _upload_queue_count
  1222-1231   _upload_queue_load
  1212-1214   _upload_queue_path
  1254-1261   _upload_queue_remove
  1233-1237   _upload_queue_save
  1267-1308   _upload_window_loop
  7619-7626   _uptime_s
 14548-14557  _url_host
   720-737    _url_ohne_zugang
   805-809    _usage_record_claude
  7840-7884   _verbindung_verloren
  6749-6780   _viewer_sample_loop
  6796-6803   _viewer_stats
 10283-10286  _wants_html
  7629-7643   _warn_empty_env
 27317-27438  _watchdog_loop
 25822-25830  _wchat_thank_ok
 18927-18957  _whisper_get_model
  7716-7723   _whisper_native_section
 18129-18135  _whisper_pool
 19026-19055  _whisper_segments
 18959-19023  _whisper_transcribe
 14872-15034  _write_restream_overlay
 26442-26522  _youtube_api_chat_loop
 20592-20695  _youtube_api_status
 20698-20765  _youtube_channel_status
 26525-26686  _youtube_chat_loop
 25682-25695  _youtube_restream_autoconfig
 25698-25722  _youtube_restream_autoconfig_inner
 25789-25817  _youtube_send
 20833-20874  _youtube_set_channel
 25725-25759  _yt_access_token
 25762-25777  _yt_live_chat_id
 26435-26439  _yt_oauth_configured
 25785-25786  _yt_sendrate_cfg
 26417-26432  _yt_timeout
  2748-2749   _ytdlp_detect_available
  2751-2762   _ytdlp_note_result
 13554-13556  _zombie_child_count
  7496-7520   about
  4111-4115   add_ai_log_entry
  4028-4031   add_archive_entry
  4727-4742   add_archive_rule
  4403-4437   add_recording
  4176-4193   add_tracking
  6139-6172   ai
  3763-3814   ai_chat
  3848-3858   ai_history_append
  3860-3865   ai_history_clear
  3837-3846   ai_history_load
  3822-3835   ai_rate_limit_check
  6201-6209   aireset
 18464-18483  azrael_chat
 26691-26813  brain_cmd
  3240-3424   build_recording_cmd
  4196-4199   bulk_add_trackings
  6993-7052   bulkadd
  8447-8587   check_all_trackings
  4248-4260   claim_live_transition
 17302-18064  class KickModerator
 15650-17065  class RestreamManager
 11831-11873  classify_proxy_anonymity
  6247-6445   cleanup
  5210-5251   cleanup_old_recordings
  4394-4401   clear_recording
 25434-25499  clip_moment
  4558-4607   compute_storage_forecast
  7115-7159   cookies_cmd
  4167-4173   count_trackings_for_chat
  4098-4109   decide_preferred_recorder
  4038-4041   delete_archive_entry
  4744-4752   delete_archive_rule
  5676-5823   diag
 26925-26986  einnahmen_cmd
  4552-4555   find_recordings_by_fingerprint
  4059-4075   finish_recording_attempt
  4220-4222   get_all_active_trackings
  4126-4129   get_all_checks
  4439-4442   get_all_recordings
  4501-4503   get_all_tags_with_counts
  4529-4532   get_annotations_for_recording
  4033-4036   get_archive_entry
  4522-4525   get_bookmarked_recordings
  1927-2044   get_cookie_health
  4489-4495   get_event_log
  4082-4096   get_last_recording_attempt
  2829-2934   get_live_status
  5010-5013   get_manual_recordings
  4537-4540   get_or_compute_inspect_sync
  5286-5330   get_outcome_breakdown
  4508-4511   get_priority_poll_interval
  4705-4714   get_profile_snapshots
  4077-4080   get_recent_recording_attempts
  4444-4447   get_recording_by_id
  4515-4518   get_recording_note
  3558-3581   get_redis
  4156-4159   get_stats
  5177-5208   get_storage_stats
  4845-4847   get_tiktok_status_distribution
  4262-4271   get_tracking_state
  4217-4218   get_trackings_for_group
  5026-5029   get_trash_recordings
  9355-10018  handle_recording_finished
  3958-3983   init_db
  5100-5154   inspect_stream_url
 21162-21164  is_revenue_platform
  4717-4725   list_archive_rules
  5480-5518   live
  7980-7988   live_check_worker
  3633-3667   llm_chat
  3690-3718   llm_chat_sync
  3675-3687   llm_list_models
  4455-4481   log_event
  1518-1551   log_recording_failure
  7309-7358   logs_cmd
 27635-28138  main
  6175-6198   on_ai_media
  7435-7461   on_ai_reply
  7464-7493   on_azrael_mention
  7525-7555   on_callback
 18489-18593  oracle_handle
  7198-7201   pause_tracking
  5340-5345   profile_keyboard
  7260-7306   quota
  8358-8425   reaper_loop
  4841-4843   record_tiktok_status
  6214-6244   recstatus
  3583-3591   redis_get_json
  3593-3599   redis_set_json
 26989-26999  report_cmd
 11876-11878  report_proxy_result
  2292-2319   resolve_tiktok_live_stream
  5021-5024   restore_recording
  7204-7207   resume_tracking
  4755-4835   run_archive_rules
 27002-27224  run_bot
 13476-13523  run_flask
  4633-4678   sample_bandwidth_for_active
  4684-4703   save_profile_snapshot
  4118-4124   save_tiktok_check
  4386-4392   set_recording_file
  4225-4229   set_tracking_paused
  5016-5019   soft_delete_recording
  8740-9353   split_and_send_video
  5393-5435   start
  4043-4057   start_recording_attempt
  6448-6486   stats
  4991-5008   stop_manual_recording
  7210-7257   stoprec
  6673-6681   summary_cmd
  7361-7432   sysres
  5825-5969   teststream
  5437-5478   tiktok
  7055-7112   topusers
  5555-5612   track
  5520-5552   track_exact
  5626-5674   tracklist
  4857-4989   trigger_manual_recording
  4347-4384   try_acquire_recording_lock
  5032-5091   universal_search
  5614-5624   untrack
 26816-26922  update_cmd
  4547-4550   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
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
